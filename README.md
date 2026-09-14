# Physical Self-Evolution

Living research website for **Universal Physical Token, robot self-improvement, VLA / action models, Online RL and embodied physical adaptation**.

## Website

**https://nkd-lkz.github.io/physical-self-evolution/**

## Current research mainline — 2026-09-14

The project has been refocused according to the latest leadership research proposal.

> **Universal Physical Token for Robot Self-Evolution**

Current question:

> Can we read a compact representation from an existing action-generation head, ground it with measured transition prediction and valid physical constraints, and use a small online learner to adapt to changing contact dynamics **without retraining the action model**?

The current source of truth is:

- [`research/physical-token-leadership-spec.md`](research/physical-token-leadership-spec.md)
- [`research/master-roadmap.md`](research/master-roadmap.md)
- [`research/rlt-multitask-benchmark.md`](research/rlt-multitask-benchmark.md) — now a baseline / validation protocol rather than the top-level research story.

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

## Initial experiment

The first controlled comparison is intentionally small:

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

## Online self-improvement scope

During the online learning phase the default contract is:

- base model frozen;
- action head frozen;
- token encoder/readout frozen;
- small actor/critic updated from actual executed actions and task rewards;
- outcome decoder trained separately from measured transitions.

This is the current operational meaning of robot self-improvement in this project.

## Existing evidence

Current block-assembly and drawer-opening/placement clips are treated as:

> **RL Token qualitative reproduction / baseline demonstrations**

They are **not** Physical Token results and are not evidence for transition loss, physics loss or universality.

Existing hammer / RoboTwin assets remain useful for regression, transition logging and controlled physics experiments, but they no longer define the top-level research story.

## Streaming RL

Streaming RL remains a later online-efficiency direction.

The current order is:

```text
RL Token / head-readout baseline
→ + transition grounding
→ + physics grounding
→ matched online adaptation
→ physical/contact shift
→ held-out model / robot
→ streaming / uncertainty-aware update later
```

We intentionally do not mix Physical Token and Streaming RL in the first ablation.

## Platform status

- **RoboTwin / existing RL Token infrastructure**: baseline and Physical Token validation platform.
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
