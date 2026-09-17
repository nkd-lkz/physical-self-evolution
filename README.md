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
- [`research/robodojo-b300-log.md`](research/robodojo-b300-log.md) — second-platform bring-up / RLinf integration log
- [`research/robodojo-contact-task-reference-selection-2026-09-17.md`](research/robodojo-contact-task-reference-selection-2026-09-17.md) — contact-task and reference selection

## Current execution gate: trustworthy B0 first

Before B1/B2, the project remains in **Gate 0 — Baseline Recovery / Validation**, but B0 Stage2 has now entered real training:

```text
Recover usable Stage1 reference
        ↓
Fix execution / timing semantics
        ↓
B0 online baseline  ← running
        ↓
B1 + measured transition loss
        ↓
B2 + valid physics loss
```

## Hammer Stage1 status

The old clean50 `pi05_base + rlt_alpha=1` long Stage1 run stopped at about 12.3k steps. Complete 6k/8k/10k/12k checkpoints were evaluated using one unified 20-seed development cohort, `H50/C50 native_macro`, the same task prompt and fixed action-sampling seed:

| checkpoint | success | rate |
|---|---:|---:|
| 6k | 8/20 | 40% |
| 8k | 7/20 | 35% |
| 10k | 8/20 | 40% |
| 12k | 10/20 | 50% |

`12k` is the current **development reference candidate**, not a final result. The curve is non-monotonic, the cohort is small, and 10/20 failures remain.

## Hammer clean500 → clean490

The original clean50 plus 450 newly collected successful demonstrations were fully exported: 500 raw/main/physics/video episodes with 500 unique seeds.

A full CPU-side quality audit found no structural, finite-value or alignment errors, but identified **10 strong action-trajectory anomalies**. Raw evidence is preserved; those 10 are excluded from new action supervision.

This yields **clean490**:

- 490 trajectory candidates;
- `train450`: 70,640 train indices;
- `eval40`: 6,238 development-validation indices;
- norm stats computed from `train450` only.

Another 10 trajectories have valid action continuity but weak contact/impulse evidence. They remain usable for Stage1 action learning, while contact/impulse-specific auxiliary supervision must use a validity mask.

`eval40` is a development validation set, not the final independent test set.

## New clean490 Stage1 — running

A fresh Stage1 recovery run has now **started** from generic `pi05_base`:

- joint VLA task adaptation + RLT reconstruction;
- `rlt_alpha=1`;
- `H=50`;
- global batch 64;
- dual-GPU data parallel;
- maximum 30k optimizer steps;
- warmup 1k;
- checkpoint every 5k;
- checkpoint selection by fixed `eval40` closed-loop capability, not minimum training loss.

Latest runtime snapshot:

> **~3798 / 30000 steps (about 12.7%)**

This is a live snapshot, not a performance result. The next meaningful gate is the first 5k checkpoint followed by the fixed eval40 closed-loop evaluation.

## B0 Stage2 — running

A new H50/C50 Stage2 baseline has started using the current 12k frozen reference candidate.

Current facts:

- action-space / observation-field transport fixes are in place;
- focused CPU tests passed;
- frozen 12k reference acceptance remains `10/20` on the matched H50/C50 development cohort;
- formal Stage2 uses 4 environments and learner batch 64;
- replay warmup target is 512 transitions;
- warmup includes critic-update preparation before online actor takeover;
- total training budget is 3000 rounds;
- **current status: warmup data collection; learner has not yet produced validated online updates.**

Therefore there is currently **no Stage2 performance-improvement claim**. The next acceptance points are learner update, version sync, actor takeover, checkpoint integrity and paired success/reward curves.

## RoboDojo second-platform status

RoboDojo has advanced to **D0–D5 complete**:

- source / assets / isolated runtime are fixed;
- B300 minimal headless RGB renderer path is validated;
- XPolicyLab CPU protocol is validated;
- native `stack_bowls / ARX X5 / joint` single-episode execution and three-camera video path are validated;
- D6–D10 remain pending: reference adapter, multi-seed Dojo-Eval, real transition bridge, RLT smoke and complete baseline.

Two contract findings matter for later RLT / Physical Token work:

1. ARX X5 arm joint state is measured `joint_pos`, while the gripper scalar is command-derived from previous control state; the full 14D vector must not be called uniformly “measured state”.
2. One policy target is internally interpolated / held across multiple simulator control items, so a policy action is **not** one physics tick. Future RLT discounting and measured-transition targets must use the real execution interval.

### RoboDojo contact-task / dynamics candidates

Current research-task recommendation:

- `plug_in_charger`: primary precision-contact / insertion candidate;
- `push_T`: friction / sliding-dynamics control task;
- `insert_key` and `insert_tubes`: later contact-rich extensions;
- `stack_bowls`: engineering regression only.

Official ARX X5 π0.5 checkpoint candidates and matching 14D norm stats have been verified to exist in the public RoboDojo data repository. They are currently **reference candidates only**: weights have not yet been restored and capability-tested on the selected contact tasks.

A further prerequisite was identified: recent upstream fixes changed RGB byte-channel handling and observation-frame alignment. Before D6/D7, the pinned local stack must be checked against the fixed stack to prevent silent color/timing mismatches.

RoboDojo remains a second platform and does not block the Hammer/RLT mainline.

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

After B0 is trustworthy:

1. **B0 — RL Token / matched head-readout baseline**
2. **B1 — B0 + measured transition loss**
3. **B2 — B1 + valid physics loss**

Matched variables include token size, learner capacity, base model, data, online interaction budget, reward, seeds and action timing.

A critical data contract is explicit:

```text
reference / proposed action
actual executed action
command state
measured state
execution duration / executed length
optional physics label + validity mask
```

These must remain distinct.

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
- New clean490 Stage1 and H50/C50 Stage2 are running, but neither has produced a validated performance-improvement result yet.
- RoboDojo D3/D5 prove renderer + native-task infrastructure paths, **not** RLinf/RLT algorithm performance.
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
    ├── robodojo-contact-task-reference-selection-2026-09-17.md
    ├── experiment-log.md
    ├── decision-log.md
    ├── frontier-landscape.md
    └── reading-program.md
```

## Knowledge-base rule

The Frontier Knowledge Base continues to track RISE, Motus2, LWD, RLT, SmoothRL, Zeva, Zetta, Astra/Harness and related work. They inform baselines and innovation boundaries, but do not override the leadership-defined actor-side Physical Token experimental contract.
