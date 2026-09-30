"""Run bounded cached-feature/module experiments, optionally sharing physical GPU 2.

This launcher never loads a VLA, starts Ray or creates a simulator. The separate
Jev queue retains exclusive-idle checks for full online training.
"""

import argparse
import fcntl
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

STORAGE = Path("/mnt/nas_ailab_434/Personal_File/luokz/rlinf_rlt_maniskill")
CODE_ROOT = Path("/home/luokz/rlinf_rlt")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", choices=("flare", "zeva", "jev"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--shared-gpu2", action="store_true")
    parser.add_argument("--fsdp", action="store_true")
    parser.add_argument("--actor-start", type=int, default=0)
    parser.add_argument("--actor-lr", type=float, default=1e-3)
    parser.add_argument(
        "--jev-data-mode", choices=("candidate", "mixed"), default="candidate"
    )
    args = parser.parse_args()
    if not 1 <= args.steps <= 1000:
        parser.error("Use 1..1000 updates per small model")
    if args.fsdp and not args.shared_gpu2:
        parser.error("The FSDP integration diagnostic requires --shared-gpu2")
    if args.task == "zeva" and args.shared_gpu2 and not args.fsdp:
        parser.error("Zeva's existing diagnostic is CPU-only")
    args.output.mkdir(parents=True, exist_ok=False)
    branch = CODE_ROOT / f"UPT_{args.task}_dev"
    sys.path.insert(0, str(branch))
    os.environ.update(
        OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1"
    )
    device = "cpu"
    gpu = None
    lock = None
    if args.shared_gpu2:
        # Coordinate with the exclusive online launcher. Other GPU jobs continue.
        lock = open("/tmp/rlt-atomic-gpu2.lock", "a")  # noqa: SIM115 -- closed after the experiment in finally.
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fields = (
            subprocess.check_output(
                [
                    "nvidia-smi",
                    "-i",
                    "2",
                    "--query-gpu=uuid,memory.free,memory.total",
                    "--format=csv,noheader,nounits",
                ],
                text=True,
                timeout=15,
            )
            .strip()
            .split(",")
        )
        uuid, free, total = fields[0].strip(), int(fields[1]), int(fields[2])
        if free < 8192:
            raise RuntimeError(
                "GPU 2 needs at least 8 GiB free for this <=2 GiB module experiment"
            )
        os.environ["CUDA_VISIBLE_DEVICES"] = uuid
        gpu = {
            "physical_index": 2,
            "uuid": uuid,
            "free_mib_before": free,
            "total_mib": total,
            "allocator_fraction_limit": 0.04,
        }
        device = "cuda:0"
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
    import torch

    torch.set_num_threads(1)
    if gpu:
        if torch.cuda.device_count() != 1 or str(
            torch.cuda.get_device_properties(0).uuid
        ).removeprefix("GPU-") != gpu["uuid"].removeprefix("GPU-"):
            raise RuntimeError("Physical GPU UUID isolation failed")
        torch.cuda.set_per_process_memory_fraction(0.04, 0)
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=branch, text=True
    ).strip()
    diff = subprocess.check_output(["git", "diff", "HEAD"], cwd=branch)
    sources = {}
    for name in ("rlinf", "toolkits/rlt"):
        for path in sorted((branch / name).rglob("*.py")):
            # Include untracked source files in provenance during development.
            sources[str(path.relative_to(branch))] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    manifest = {
        "task": args.task,
        "device": device,
        "gpu": gpu,
        "git_revision": revision,
        "tracked_diff_sha256": hashlib.sha256(diff).hexdigest(),
        "source_sha256": sources,
        "torch": torch.__version__,
        "updates_per_model": 20 if args.fsdp else args.steps,
        "experiment_kind": "single_rank_fsdp" if args.fsdp else "mechanism_diagnostic",
        "status": "running",
    }
    path = args.output / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    start = time.monotonic()
    try:
        if args.fsdp:
            from fsdp_modules import run

            run(args.task, args.output / "models", device)
        elif args.task == "flare":
            from toolkits.rlt.ablate_action_input import run

            data = STORAGE / "research/flare_step2000_pilot_20260930_005943"
            run(
                data / "direct/train_config.yaml",
                data / "test_cache",
                args.output / "models",
                device=device,
                steps=args.steps,
            )
        elif args.task == "jev":
            from toolkits.rlt.compare_residual import run

            run(
                args.output / "models",
                device=device,
                steps=args.steps,
                data_mode=args.jev_data_mode,
                actor_start=args.actor_start,
                actor_lr=args.actor_lr,
            )
        else:
            from toolkits.rlt.probe_memory_dynamics import audit_empirical, fit

            data = STORAGE / "research/zeva_hidden_dynamics_20260927"
            fit(data, args.output / "models", updates=args.steps)
            audit_empirical(data, args.output / "empirical")
        manifest["status"] = "completed"
    except BaseException as exc:
        manifest.update(status="failed", error=f"{type(exc).__name__}: {exc}")
        raise
    finally:
        manifest["seconds"] = time.monotonic() - start
        if gpu:
            manifest["max_reserved_mib"] = torch.cuda.max_memory_reserved() / 2**20
            manifest["max_allocated_mib"] = torch.cuda.max_memory_allocated() / 2**20
        path.write_text(json.dumps(manifest, indent=2) + "\n")
        if lock:
            lock.close()


if __name__ == "__main__":
    main()
