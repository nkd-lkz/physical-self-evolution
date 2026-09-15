# Physical Self-Evolution

Living research website for **Universal Physical Token, robot self-improvement, VLA / action models, Online RL and embodied physical adaptation**.

## Website

**https://nkd-lkz.github.io/physical-self-evolution/**

## Current research mainline — 2026-09-15

The project is aligned to the leadership-defined research proposal:

> **Universal Physical Token for Robot Self-Evolution**

Current question:

> Can we read a compact representation from an existing action-generation head, ground it with measured transition prediction and valid physical constraints, and use a small online learner to adapt to changing contact dynamics **without retraining the action model during online adaptation**?

Current source of truth:

- [`research/physical-token-leadership-spec.md`](research/physical-token-leadership-spec.md)
- [`research/master-roadmap.md`](research/master-roadmap.md)
- [`research/rlt-multitask-benchmark.md`](research/rlt-multitask-benchmark.md)
- [`research/progress-2026-09-15.md`](research/progress-2026-09-15.md) — latest execution snapshot

## Current execution gate: recover a trustworthy B0 baseline first

Before B1/B2, the project remains in **Gate 0 — Baseline Recovery**:

```text
Recover a usable Stage1 reference
        ↓
Fix RoboTwin execution / timing semantics
        ↓
Establish a trustworthy B0 online baseline
        ↓
B1 + measured transition loss
        ↓
B2 + valid physics loss
```

Two separate issues remain tracked:

1. **Execution protocol** — current hammer Stage1 uses `H=50`; RoboTwin native TOPP with `H50/C50` is the current capability anchor. Historical `H50/C10` changes replanning boundaries and is kept as a diagnostic setting.
2. **Stage1 capability** — paired H50/C50 evaluation contains a case where SFT20k succeeds and the old Stage1 2k fails, while a positive-control seed shows both can succeed. This motivates recovery but does not prove training budget is the unique root cause.

## Live execution snapshot — 2026-09-15 13:29 UTC

### Hammer Stage1 20k

A new `pi05_base + rlt_alpha=1` joint Stage1 is **running**:

- target: 20,000 optimizer steps;
- 2-GPU data parallel;
- global batch 64 / micro batch 2;
- gradient accumulation 16 per rank;
- warmup 1,000;
- checkpoint every 2,000 steps;
- `H=50`.

Snapshot:

- `2459 / 20000` steps;
- step-2000 checkpoint saved;
- latest `loss/rlt/vla/grad = 0.254 / 0.252 / 0.00251 / 1.27`;
- run not finished, so capability recovery is **not** yet accepted.

Checkpoint selection will use fixed-seed `H50/C50` closed-loop capability curves (`2k / 4k / ... / 20k`), not minimum training loss.

### Hammer clean500 data expansion

- target: 500 successful expert trajectories;
- snapshot: `160 / 500` successful **raw trajectories**;
- 110 are newly collected beyond the original clean50;
- final HDF5 / physics sidecar / video export has not yet reached 160 episodes.

After raw collection completes:

- fixed split: `train450 / val50`;
- norm stats use **train450 only**;
- no clean500 training starts before conversion / split / norm validation finishes.

### RoboDojo

RoboDojo has moved beyond “not tested”:

- **D0 complete**: source / system manifest;
- **D1 complete**: fixed submodules + ~66 GB assets, doctor `13 PASS / 4 WARN / 0 FAIL`;
- **D2 complete**: independent Isaac Sim / Isaac Lab runtime, doctor `14 PASS / 3 WARN / 0 FAIL`;
- **D4 complete**: XPolicyLab CPU WebSocket closed loop, 10 episodes × 20 action steps = 200 steps; ARX X5 joint schema = 14D float32, chunk length 2;
- **D3 pending**: no B300 headless RGB renderer/device acceptance yet;
- D5 native task, D6–D7 Dojo-Eval, D8–D9 Dojo-RL, D10 baseline are still pending.

Simulator and policy runtimes are intentionally isolated because their Python dependency constraints conflict.

## Core architecture

```text
Frozen action model
      ↓
Action-head pre-output features
      + robot history
      + robot metadata
      ↓
Lightweight model/robot adapters
      ↓
Fixed-size Physical Token z_t
      ↓
Small online actor / critic
      ↓
Behavior adaptation
```

Representation objective:

```text
L_token = L_ro + λ_dyn L_dyn + λ_phys L_phys
```

- `L_ro`: readout / reconstruction from stop-gradient action-head features;
- `L_dyn`: action-conditioned prediction of measured physical transitions;
- `L_phys`: valid physical constraints, starting from kinematic consistency and actuator feasibility.

Contact / friction / rigid-body residuals are optional and require valid sensing, models and calibration.

## Initial Physical Token experiment

After Gate 0 is stable:

1. **B0 — RL Token / matched head-readout baseline**
2. **B1 — B0 + measured transition loss**
3. **B2 — B1 + valid physics loss**

Matched variables include token size, learner capacity, base model, data, online interaction budget, reward, seeds and action timing.

## What “Universal” currently means

Universal is an **empirical hypothesis**, not a result:

- shared token shape;
- shared physical objectives;
- lightweight adapters for model families and embodiments.

Cross-model / cross-robot claims require held-out tests.

## Existing evidence

- Block-assembly and drawer-opening/placement clips are **RL Token qualitative reproduction**, not Physical Token results.
- Old hammer Stage2 proves rollout → replay → actor/critic update → weight sync → checkpoint engineering, but not a usable B0 performance baseline.
- Expert reward probing produced a positive success/reward case, so the task is not known to be reward-dead.
- clean500 and RoboDojo progress are infrastructure/data advances, not Physical Token algorithm gains.

## Platform status

- **RoboTwin / RL Token infrastructure**: current Gate 0 and Physical Token validation platform.
- **RoboDojo**: second platform; source/assets/runtime and CPU policy protocol are validated, while B300 renderer/device compatibility remains unverified until D3.

## Public repository policy

This is a **public, redacted research log**.

We publish scientific design, sanitized metrics, public SHAs / branches and research conclusions. We do not publish internal absolute paths, usernames, host/IP information, credentials, private dashboard identifiers or unnecessary infrastructure commands.

See [`research/knowledge-base-maintenance.md`](research/knowledge-base-maintenance.md).

## Repository structure

```text
.
├── index.html
├── reader.html
├── assets/
├── data/
├── notes/
├── archive/
└── research/
    ├── physical-token-leadership-spec.md
    ├── master-roadmap.md
    ├── rlt-multitask-benchmark.md
    ├── progress-2026-09-15.md
    ├── robodojo-b300-log.md
    ├── experiment-log.md
    ├── decision-log.md
    ├── frontier-landscape.md
    └── reading-program.md
```

## Knowledge-base rule

The Frontier Knowledge Base continues to track RISE, Motus2, LWD, RLT, SmoothRL, Zeva, Zetta and related work. They inform baselines and innovation boundaries, but do not override the leadership-defined Physical Token experimental contract.
