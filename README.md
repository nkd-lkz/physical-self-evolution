# Physical Self-Evolution

Living research website for **Universal Physical Token, robot self-improvement, VLA / action models, Online RL and embodied physical adaptation**.

## Website

**https://nkd-lkz.github.io/physical-self-evolution/**

## Current research mainline — 2026-09-15

The project is aligned to the leadership-defined research proposal:

> **Universal Physical Token for Robot Self-Evolution**

Current question:

> Can we read a compact representation from an existing action-generation head, ground it with measured transition prediction and valid physical constraints, and use a small online learner to adapt to changing contact dynamics **without retraining the action model during online adaptation**?

The current source of truth is:

- [`research/physical-token-leadership-spec.md`](research/physical-token-leadership-spec.md)
- [`research/master-roadmap.md`](research/master-roadmap.md)
- [`research/rlt-multitask-benchmark.md`](research/rlt-multitask-benchmark.md) — baseline / validation protocol
- [`research/progress-2026-09-15.md`](research/progress-2026-09-15.md) — latest baseline recovery status

## Current execution gate: recover a trustworthy B0 baseline first

Before implementing B1/B2, the project is currently in **Gate 0 — Baseline Recovery**:

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

Two separate issues are now tracked:

1. **Execution protocol** — existing hammer Stage1 uses `H=50`; RoboTwin native TOPP execution under `H50/C50` is the current capability anchor. Historical `H50/C10` changes replanning boundaries and is kept as a diagnostic setting, not a fair reference capability result.
2. **Stage1 capability** — the old base-init Stage1 used only 2k optimizer steps / global batch32, while standalone task-SFT used 20k / batch64. Paired H50/C50 evaluation shows at least one scene where SFT succeeds and the old Stage1 fails, while an additional positive-control scene shows both can succeed. This motivates stronger Stage1 recovery, but does **not** prove training budget is the unique root cause.

## Current Stage1 recovery experiment

The next baseline run is configured as:

- generic `pi05_base` initialization;
- `rlt_alpha=1`;
- joint VLA task adaptation + RLT reconstruction;
- `H=50`;
- 20,000 optimizer steps;
- 2-GPU data parallel;
- global batch 64 / micro batch 2;
- gradient accumulation 16 per rank;
- warmup 1,000 steps;
- checkpoint every 2,000 steps.

The configuration dry-run has passed. **The full GPU training is still pending and is not recorded as completed.**

Checkpoint selection will use fixed-seed `H50/C50` closed-loop capability curves (`2k / 4k / ... / 20k`), not minimum training loss.

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

The representation objective is:

```text
L_token = L_ro + λ_dyn L_dyn + λ_phys L_phys
```

- `L_ro`: readout / reconstruction from stop-gradient action-head features;
- `L_dyn`: action-conditioned prediction of measured physical transitions;
- `L_phys`: only valid physical constraints, starting from kinematic consistency and actuator feasibility.

Contact / friction / rigid-body residuals are optional and require valid sensing, models and calibration.

## Initial Physical Token experiment

After Gate 0 is stable, the first controlled comparison remains:

1. **B0 — RL Token / matched head-readout baseline**
2. **B1 — B0 + measured transition loss**
3. **B2 — B1 + valid physics loss**

Keep matched:

- token size;
- learner capacity;
- base action model;
- data;
- online interaction budget;
- task reward;
- seeds;
- action chunk / timing.

Measure:

- task success;
- physical violations;
- adaptation cost / time;
- old-task retention;
- repeated seeds and uncertainty intervals.

## What “Universal” currently means

Universal is currently a **research hypothesis**, not a result.

It means:

- shared token shape;
- shared physical objectives;
- lightweight adapters for different model families and robot embodiments.

Cross-model and cross-robot transfer must be demonstrated on held-out model-head families and held-out embodiments before being claimed.

## Existing evidence

- Existing block-assembly and drawer-opening/placement clips are **RL Token qualitative reproduction / baseline demonstrations**, not Physical Token results.
- Hammer data / norm / checkpoints / transition logging remain valuable baseline infrastructure.
- The old Stage2 run proved rollout → replay → actor/critic update → weight sync → checkpoint engineering, but its zero-reward episodes do **not** establish a usable B0 performance baseline.
- Expert reward probing has produced a positive success/reward example, so the current evidence does not support the claim that the task can never emit positive reward.

## Streaming RL

Streaming RL remains a later online-efficiency direction.

The current order is:

```text
Gate 0: trustworthy RL Token baseline
→ + transition grounding
→ + physics grounding
→ matched online adaptation
→ physical/contact shift
→ held-out model / robot
→ streaming / uncertainty-aware update later
```

We intentionally do not mix Physical Token and Streaming RL in the first ablation.

## Platform status

- **RoboTwin / existing RL Token infrastructure**: current baseline and Physical Token validation platform.
- **RoboDojo on B300**: side track only; current status remains **not yet tested on this machine**. No compatibility claim is recorded without local evidence.

## Public repository policy

This is a **public, redacted research log**.

We publish scientific design, sanitized metrics, public SHAs / branches and research conclusions. We do not publish internal absolute paths, usernames, IPs, credentials, private dashboard identifiers or unnecessary infrastructure details.

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
    ├── progress-2026-09-12.md
    ├── robodojo-b300-log.md
    ├── experiment-log.md
    ├── decision-log.md
    ├── frontier-landscape.md
    └── reading-program.md
```

## Knowledge-base rule

The Frontier Knowledge Base continues to track RISE, Motus2, LWD, RLT, SmoothRL, Zeva, Zetta and related work.

These papers are used to understand baselines and innovation boundaries, but they do not override the leadership-defined Physical Token experimental contract.
