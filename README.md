# Physical Self-Evolution

Living research website for **Universal Physical Token, robot self-improvement, VLA / action models, Online RL and embodied physical adaptation**.

## RSI survey literature

[具身 / 机器人 RSI 综述调研](survey-rsi/README.md) — 每日增量、原图阅读卡片、去重索引和证据核查，与实验主线分别维护。

## Website

**https://nkd-lkz.github.io/physical-self-evolution/**

## Current research mainline — 2026-09-18

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
- [`research/progress-2026-09-18.md`](research/progress-2026-09-18.md) — latest execution snapshot
- [`research/progress-2026-09-17.md`](research/progress-2026-09-17.md) — previous detailed snapshot
- [`research/robodojo-b300-log.md`](research/robodojo-b300-log.md) — second-platform bring-up / RLinf integration log
- [`research/robodojo-contact-task-reference-selection-2026-09-17.md`](research/robodojo-contact-task-reference-selection-2026-09-17.md) — contact-task and reference selection

## Current execution gate: trustworthy B0 first

Before B1/B2, the project remains in **Gate 0 — Baseline Recovery / Validation**. A first H50/C50 B0 Stage2 run has now been stopped after online degradation, so the immediate task is **B0 diagnosis**, not Physical Token:

```text
Recover / validate Stage1 reference
        ↓
Fix execution / timing semantics
        ↓
B0 online baseline
        ↓
BC/reference/Q diagnosis  ← current
        ↓
trustworthy B0
        ↓
B1 + measured transition loss
        ↓
B2 + valid physics loss
```

The current rule is simple: **do not interpret Stage2 parameter updates as algorithmic progress unless the trained actor at least preserves or improves the matched frozen reference.**

## Hammer Stage1 status

Two Stage1 lines are now tracked separately.

### Old clean50 reference line

The old clean50 `pi05_base + rlt_alpha=1` run stopped around 12.3k. On the unified 20-seed `H50/C50 native_macro` development cohort:

| checkpoint | success | rate |
|---|---:|---:|
| 6k | 8/20 | 40% |
| 8k | 7/20 | 35% |
| 10k | 8/20 | 40% |
| 12k | 10/20 | 50% |

The old 12k remains a development reference anchor, not a final reference.

### New clean490 / train450 line

A fresh generic-`pi05_base` joint VLA+RLT Stage1 run was launched on train450 and later stopped for migration at about **10823 / 30000** steps. Complete 5k and 10k checkpoints were preserved.

The 10k checkpoint was evaluated twice under the same eval40 protocol on two allowed GPUs:

> **22 / 40 = 55% success in both runs**

The two runs also matched on aggregate return (~0.55) and mean episode length (~196.25). This supports aggregate reproducibility under the current development protocol, but it is **not** an independent 80-seed result and does not by itself prove that train450 is significantly better than the old clean50 line.

The next reference work is failure-stage review, matched-seed checkpoint comparison and independent-seed validation.

## Hammer clean500 → clean490

The data contract remains:

- 500 raw demonstrations preserved;
- 10 strong action-trajectory anomalies excluded from new supervision;
- **clean490 = train450 + eval40**;
- train450 provides 70,640 training indices;
- eval40 provides 6,238 development-validation indices;
- normalization uses train450 only;
- another 10 trajectories remain valid for action learning but have weak contact/impulse labels, so contact-specific auxiliary targets require a validity mask.

The dataset audit strengthens supervision quality, but does not itself prove better task success.

## New clean490 Stage1 — stopped after 10k checkpoint

The fresh clean490 Stage1 run used:

- generic `pi05_base`;
- joint VLA task adaptation + RLT reconstruction;
- `rlt_alpha=1`;
- H50;
- global batch64;
- dual-GPU data parallel;
- intended maximum 30k optimizer steps;
- checkpoint every5k.

It was actively stopped at about **10823 steps** for migration. This is not a completed 30k run.

Latest saved training-health values were approximately:

- total loss 0.05317;
- RLT loss 0.05236;
- VLA loss 0.000808.

Checkpoint choice remains based on closed-loop capability, not minimum training loss. The 10k checkpoint currently has the strongest new-line evidence: two eval40 runs at 22/40 each.

## B0 Stage2 — stopped after online degradation

The first new H50/C50 B0 Stage2 run used the old clean50/12k frozen reference.

Reference anchor:

> **10 / 20 = 50%** on the matched development cohort.

Stage2 used a direct normalized actor, 4 training environments, batch64, replay warmup and a 4:1 critic:actor update ratio. During periodic 20-seed evaluation:

- around rounds 200/300: ~45%;
- around rounds 800/900: ~15%.

The run was actively stopped around outer round 985. The low final critic / BC losses are **not** accepted as evidence that Q-values or the actor are correct.

Current interpretation:

> **This B0 configuration degrades the frozen reference and is therefore not yet a trustworthy online baseline.**

Next: BC-only / reference-consistency, action-deviation, reference-dropout, BC/Q-balance and critic-calibration diagnostics. No further budget is added to the same configuration until those checks are complete.

## RoboDojo second-platform status

RoboDojo status is unchanged from the latest 9/17 validation:

- D0–D5 complete at the infrastructure/native-task level;
- D6 real reference-only adapter pending;
- D7 multi-seed Dojo-Eval pending;
- D8 real transition alignment pending;
- online RLT not yet started.

Current task candidates remain:

- `plug_in_charger`: primary precision-contact candidate;
- `push_T`: friction / dynamics control;
- `insert_key` / `insert_tubes`: later contact-rich extensions;
- `stack_bowls`: engineering regression only.

The official ARX X5 π0.5 candidates still require version compatibility checks, model restoration and actual capability evaluation before they can serve as D6 references.

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

- Block-assembly and drawer-opening/placement clips remain **RL Token qualitative reproduction**, not Physical Token results.
- Old clean50 Stage1 provides a partial reference capability curve; 12k reached 10/20 on its 20-seed development cohort.
- New train450 Stage1 10k reached **22/40 twice** on eval40; this is development evidence, not a final independent comparison.
- The first H50/C50 B0 Stage2 run **degraded** from about 45% periodic success to about 15% and was stopped; this is evidence that the current online learner configuration is not yet trustworthy.
- clean490 strengthens data quality and label validity but does not itself prove task improvement.
- RoboDojo D3/D5 prove renderer + native-task infrastructure paths, not RLinf/RLT algorithm performance.
- **No validated online-RL gain and no Physical Token / physics-grounding gain exists yet.**

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
    ├── progress-2026-09-18.md
    ├── progress-2026-09-17.md
    ├── robodojo-b300-log.md
    ├── robodojo-contact-task-reference-selection-2026-09-17.md
    ├── experiment-log.md
    ├── decision-log.md
    ├── frontier-landscape.md
    └── reading-program.md
```

## Literature map & reading ledger

The Physical Token literature review is now maintained as a first-class research asset rather than an ad-hoc paper list:

- **Direction map / mental model:** [`research/literature/physical-token-direction-map.md`](research/literature/physical-token-direction-map.md)
- **125-paper master audit:** [`research/literature/physical-token-literature-audit-2026-09-19.md`](research/literature/physical-token-literature-audit-2026-09-19.md)
- **Read / unread / priority ledger:** [`research/literature/reading-ledger.md`](research/literature/reading-ledger.md)
- **Machine-readable ledger:** [`data/literature-reading-ledger.json`](data/literature-reading-ledger.json)
- **Deep-note index:** [`notes/README.md`](notes/README.md)

Every catalogued paper has at least a **search/abstract mini-note** containing method, project relevance, verification boundary and first-party source. A paper is marked “read” or “deep-read” only after actual method/experiment review; the remaining entries stay explicitly queued rather than being treated as understood.

Current reading priority is collision avoidance around **action-side representations, future/consequence supervision, hidden-dynamics adaptation, physical constraints, value guidance, WAM interfaces and cross-head transfer**.

## Knowledge-base rule

The Frontier Knowledge Base continues to track RISE, Motus2, LWD, RLT, SmoothRL, Zeva, Zetta, Astra/Harness and related work. They inform baselines and innovation boundaries, but do not override the leadership-defined actor-side Physical Token experimental contract.
