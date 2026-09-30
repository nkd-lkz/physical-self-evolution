"""Exercise actual RLT loss paths under single-rank FSDP, without Ray or VLA."""

import copy
import json
from pathlib import Path


def run(branch: str, output: Path, device: str) -> dict:
    """Check update and checkpoint contracts; synthetic transitions are not RL evidence."""
    import torch
    import torch.distributed as dist
    from omegaconf import OmegaConf
    from rlinf.models.embodiment.base_policy import ForwardType
    from rlinf.models.embodiment.mlp_policy.rlt_mlp_policy import RLTMLPPolicy
    from rlinf.workers.actor.fsdp_rlt_ac_policy_worker import RLTACLossMixin
    from torch.distributed.fsdp import FullyShardedDataParallel as FSDP

    output.mkdir(parents=True, exist_ok=False)
    torch.manual_seed(73)
    torch.cuda.set_device(0)
    dist.init_process_group(
        "nccl", init_method=f"file://{output / 'rendezvous'}", rank=0, world_size=1
    )
    try:
        common = {"z_dim": 8, "proprio_dim": 9, "action_dim": 8, "num_action_chunks": 2}
        model_cfg = {**common, "model_type": "rlt_mlp_policy", "q_head_type": "default"}
        obs = {
            "z_rl": torch.randn(4, 8, device=device),
            "proprio": torch.randn(4, 9, device=device),
            "ref_chunk": torch.zeros(4, 2, 8, device=device),
        }
        algorithm = {
            "gamma": 0.9,
            "bc_weight": 1.0,
            "q_weight": 1.0,
            "loss_type": "rlt_ac",
            "reference_dropout_prob": 0.0,
        }
        if branch == "flare":
            from rlinf.models.embodiment.modules.rlt_latent_world import (
                LatentWorldConfig,
                RLTLatentWorld,
            )

            world = RLTLatentWorld(
                LatentWorldConfig(
                    z_dim=8,
                    proprio_dim=9,
                    action_dim=8,
                    chunk_len=2,
                    horizons=(1, 2),
                    hidden_dim=16,
                    num_heads=2,
                    num_layers=1,
                )
            )
            checkpoint = output / "world.pt"
            torch.save(world.checkpoint({"diagnostic": True}), checkpoint)
            options = {"enabled": True, "checkpoint": str(checkpoint)}
            model_cfg["latent_world"] = options
            algorithm["latent_world_weight"] = 1.0
            model = RLTMLPPolicy(**common, latent_world=options)
        elif branch == "zeva":
            from dataclasses import asdict

            from rlinf.algorithms.rlt.interaction_memory import (
                InteractionMemory,
                InteractionMemoryConfig,
            )

            c = InteractionMemoryConfig(chunk_len=2)
            memory = InteractionMemory(c)
            memory.begin_attempt("synthetic")
            memory.append_completed(
                torch.zeros(9), torch.full((2, 8), 0.1), torch.full((9,), 0.01)
            )
            obs.update(
                {
                    k: v[None].repeat(4, *([1] * v.ndim)).to(device)
                    for k, v in memory.snapshot(torch.zeros(9)).items()
                }
            )
            model = RLTMLPPolicy(
                **common, interaction_memory={"enabled": True, **asdict(c)}
            )
        else:
            from rlinf.models.embodiment.mlp_policy.rlt_atomic_policy import (
                RLTAtomicPolicy,
            )

            model_cfg["atomic_decision"] = {"enabled": True}
            model = RLTAtomicPolicy(**common, atomic_decision={"radius": 0.08})
        model = model.to(device)
        target = copy.deepcopy(model)
        initial = {n: p.detach().clone() for n, p in model.named_parameters()}
        wrapped = FSDP(model, device_id=0, use_orig_params=True)
        worker = RLTACLossMixin()
        worker.model, worker.target_model, worker.torch_dtype = (
            wrapped,
            target,
            torch.float32,
        )
        worker.cfg = OmegaConf.create(
            {
                "actor": {"model": model_cfg},
                "algorithm": algorithm,
                "env": {
                    "train": {
                        "env_type": "maniskill_rlt",
                        "init_params": {"control_mode": "pd_joint_delta_pos"},
                    }
                },
                "rollout": {"model": model_cfg},
            }
        )
        critic_names = ("q_head", "latent_world", "memory_encoder")
        critic = [
            p
            for n, p in wrapped.named_parameters()
            if any(k in n for k in critic_names)
        ]
        actor = [
            p
            for n, p in wrapped.named_parameters()
            if not any(k in n for k in critic_names)
        ]
        optimizers = [
            torch.optim.Adam(critic, lr=1e-3),
            torch.optim.Adam(actor, lr=1e-3),
        ]
        next_obs = {k: v.clone() for k, v in obs.items()}
        next_obs["z_rl"] += 0.1
        next_obs["proprio"] += 0.01
        batch = {
            "curr_obs": obs,
            "next_obs": next_obs,
            "actions": torch.rand(4, 16, device=device) * 0.2,
            "rewards": torch.ones(4, 2, device=device),
            "dones": torch.zeros(4, 2, dtype=torch.bool, device=device),
            "terminations": torch.zeros(4, 2, dtype=torch.bool, device=device),
        }
        losses = []
        for _ in range(20):
            for name, optimizer, params in zip(
                ("forward_critic", "forward_actor"), optimizers, (critic, actor)
            ):
                wrapped.zero_grad(set_to_none=True)
                method = getattr(RLTACLossMixin, name)
                while hasattr(method, "__wrapped__"):
                    method = method.__wrapped__
                loss = method(worker, batch)[0]
                loss.backward()
                torch.nn.utils.clip_grad_norm_(params, 10.0, error_if_nonfinite=True)
                optimizer.step()
                losses.append(float(loss.detach()))
        weights = {k: v.cpu() for k, v in wrapped.state_dict().items()}
        torch.save(weights, output / "weights.pt")
        target.load_state_dict(
            torch.load(output / "weights.pt", weights_only=True, map_location=device)
        )
        with torch.no_grad():
            before = wrapped(forward_type=ForwardType.SAC, obs=obs, deterministic=True)[
                0
            ]
            after = target(forward_type=ForwardType.SAC, obs=obs, deterministic=True)[0]
            torch.testing.assert_close(before, after)
        changed = {
            n: float((p.detach() - initial[n]).abs().max())
            for n, p in model.named_parameters()
        }
        assert any(v > 0 for n, v in changed.items() if "q_head" in n)
        if branch == "flare":
            assert any(v > 0 for n, v in changed.items() if "latent_world.encoder" in n)
        elif branch == "zeva":
            assert any(v > 0 for n, v in changed.items() if "memory_encoder" in n)
        else:
            assert any(v > 0 for n, v in changed.items() if "selector" in n)
        report = {
            "branch": branch,
            "scope": "Single-rank fp32 FSDP + synthetic transitions, 20 critic/actor updates; no Ray, simulator, VLA, or multi-rank verification",
            "losses": losses,
            "parameter_max_delta": changed,
            "checkpoint_action_parity": True,
        }
        (output / "results.json").write_text(
            json.dumps(report, indent=2, allow_nan=False) + "\n"
        )
        return report
    finally:
        dist.destroy_process_group()
