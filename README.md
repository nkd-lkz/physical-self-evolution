# Physical Self-Evolution

Living research website for **Universal Physical Token, robot self-improvement, VLA / action models, Online RL and embodied physical adaptation**.

## Website

**https://nkd-lkz.github.io/physical-self-evolution/**

## Current research mainline — 2026-09-17

The project is aligned to the leadership-defined research proposal:

> **Universal Physical Token for Robot Self-Evolution**

Current question:

> Can we extract a compact, reusable representation from an existing actor / action-generation head, ground it with measured transition prediction and valid physical constraints, and use a small online learner to improve physical adaptation and final task success **without retraining the action model during online adaptation**?

### Scope boundary: actor-side token, not planner-side orchestration

- GPT-6 Astra / Harness-style systems are mainly **planner / reviewer / orchestration** approaches around an existing policy;
- this project is **not** trying to win by adding a stronger planner;
- the core object is an **actor-side universal compact token** extracted from the action model itself;
- planner/harness work remains Frontier reference for failure diagnosis, operating-range reasoning and validation-gated recovery.

```text
actor / action-generation features
        ↓
Universal Physical Token
        ↓
transition / physics grounding
        ↓
small online learner
        ↓
final physical-task success / adaptation gain
```

LLM planner, memory, zero-shot reasoning and skill-harness evolution are **not first-round B0/B1/B2 variables**.

Current source of truth:

- [`research/physical-token-leadership-spec.md`](research/physical-token-leadership-spec.md)
- [`research/master-roadmap.md`](research/master-roadmap.md)
- [`research/rlt-multitask-benchmark.md`](research/rlt-multitask-benchmark.md)
- [`research/progress-2026-09-17.md`](research/progress-2026-09-17.md) — latest execution snapshot

## Current execution gate: trustworthy B0 first

Before B1/B2, the project remains in **Gate 0 — Baseline Recovery / Validation**:

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

### Stage1 capability curve — 2026-09-17

The old clean50 `pi05_base + rlt_alpha=1` long Stage1 run stopped at about 12.3k steps, so the originally planned 20k run was **not completed**. Complete 6k/8k/10k/12k checkpoints were evaluated using one unified 20-seed development cohort, `H50/C50 native_macro`, the same task prompt and fixed action-sampling seed:

| checkpoint | success | rate |
|---|---:|---:|
| 6k | 8/20 | 40% |
| 8k | 7/20 | 35% |
| 10k | 8/20 | 40% |
| 12k | 10/20 | 50% |

`12k` is the current **development reference candidate**, not a final result. The curve is non-monotonic, the cohort is small, and 10/20 failures remain. These results prove partial closed-loop capability but do not prove that Stage1 generalization is solved or that training budget is the unique root cause.

A full-physics 12k video/trace capture on the same cohort is prepared for failure-stage analysis but has not yet been run.

## Hammer clean500 → clean490

The original clean50 plus 450 newly collected successful demonstrations have now been fully exported: 500 raw/main/physics/video episodes with 500 unique seeds.

A full CPU-side quality audit decoded all numeric fields, all four-camera RGB frames and all MP4 frames. File structure, finite values and temporal alignment passed, but **10 action trajectories showed strong motion discontinuities / branch-jump anomalies**. Raw evidence is preserved; those 10 are excluded from new action supervision.

This yields **clean490**:

- 490 trajectory candidates;
- `train450`: 70,640 train indices;
- `eval40`: 6,238 development-validation indices;
- norm stats computed from `train450` only.

Another 10 trajectories have valid action continuity but weak/nonzero-impulse contact evidence. They remain usable for Stage1 action learning, while contact/impulse-specific auxiliary supervision must use a validity mask. A missing impulse label is **not** treated as a reliable “no contact / failed task” negative.

`eval40` is a development validation set, not the final independent test set, because some seeds were previously used during checkpoint development.

## New clean490 Stage1 preparation

A fresh Stage1 recovery run is prepared from generic `pi05_base`:

- joint VLA task adaptation + RLT reconstruction;
- `rlt_alpha=1`;
- `H=50`;
- global batch 64;
- dual-GPU data parallel;
- default maximum **30k optimizer steps**;
- warmup 1k;
- checkpoint every 5k;
- checkpoint selection by fixed `eval40` closed-loop capability, not minimum training loss.

Dataset conversion, train-only normalization, OpenPI loader checks, Hydra train/eval dry-runs and focused CPU tests are complete. **The new GPU training has not started yet.**

## RoboDojo

RoboDojo status is unchanged from the previous gate review:

- **D0 complete**: source / system manifest;
- **D1 complete**: fixed submodules + assets;
- **D2 complete**: independent Isaac Sim / Isaac Lab runtime;
- **D4 complete**: XPolicyLab CPU WebSocket protocol loop;
- **D3 pending**: no B300 headless RGB renderer/device acceptance yet;
- D5 native task, D6–D7 Dojo-Eval, D8–D9 Dojo-RL, D10 baseline remain pending.

RoboDojo is a second platform and does not block the current Hammer/RLT baseline and Physical Token hypothesis tests.

## Core architecture

```text
Frozen action model / actor
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
- `L_dyn`: action-conditioned prediction of **measured** physical transitions using actual/executed actions;
- `L_phys`: valid physical constraints, starting from kinematic consistency and actuator feasibility.

Contact / friction / rigid-body / force targets are optional and require valid sensing, models, calibration and per-label validity masks.

## Initial Physical Token experiment

After Gate 0 is stable:

1. **B0 — RL Token / matched head-readout baseline**
2. **B1 — B0 + measured transition loss**
3. **B2 — B1 + valid physics loss**

Matched variables include token size, learner capacity, base model, data, online interaction budget, reward, seeds and action timing.

A critical data contract is now explicit:

```text
reference / proposed action
actual executed action
command state
measured state
```

These must remain distinct. The current Stage1 imitation dataset keeps the original command-state semantics; B1 must explicitly source measured state / executed consequences rather than silently reusing command targets.

## What “Universal” currently means

Universal is an **empirical hypothesis**, not a result:

- shared token shape;
- shared physical objectives;
- lightweight adapters for model families and embodiments.

Cross-model / cross-robot claims require held-out tests.

## Existing evidence

- Block-assembly and drawer-opening/placement clips are **RL Token qualitative reproduction**, not Physical Token results.
- Old hammer Stage2 proves rollout → replay → actor/critic update → weight sync → checkpoint engineering, but not a usable B0 performance baseline.
- The unified Stage1 20-seed curve demonstrates partial reference capability; 12k is only a development candidate.
- clean490 strengthens data quality and supervision validity; it does not yet prove better task success.
- Astra / Harness / SHAPER results are planner/harness references, not direct evidence that the actor-side Physical Token hypothesis is correct.

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
    ├── progress-2026-09-17.md
    ├── robodojo-b300-log.md
    ├── experiment-log.md
    ├── decision-log.md
    ├── frontier-landscape.md
    └── reading-program.md
```

## Knowledge-base rule

The Frontier Knowledge Base continues to track RISE, Motus2, LWD, RLT, SmoothRL, Zeva, Zetta, Astra/Harness and related work. They inform baselines and innovation boundaries, but do not override the leadership-defined actor-side Physical Token experimental contract.
