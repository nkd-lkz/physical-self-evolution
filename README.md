# Physical Self-Evolution

Living research website for **Physical Interaction, Embodied Self-Evolution, VLA, Online RL, Memory / ICL, Failure Recovery and robot learning experiments**.

## Website

**https://nkd-lkz.github.io/physical-self-evolution/**

## Current research phase

### Phase 0 — RLT Multi-task Benchmark **← current**
Build a reproducible multi-task VLA + Online RL research bench on RoboTwin 2.0.

Current execution order:

1. finish the first **RoboTwin 2.0 / RLinf_support pinned** RLT Stage 1/2 baseline;
2. validate real `C=10` Stage 2 rollout / replay / actor-critic updates;
3. freeze the first baseline;
4. migrate to RoboTwin 2.0 `main` bridge;
5. expand to additional contact mechanisms and only then move to diagnosis / novelty.

### Latest verified progress — 2026-09-12

- hammer task-SFT checkpoint quick sweep completed: 5k/10k/15k/20k = 1/4, 0/4, 2/4, 2/4; action-sampling RNG is not yet fixed, so these are development-screening results only;
- paper-aligned **generic π0.5 base-init RLT Stage 1 1-step smoke passed**: total/RLT/VLA loss = 3.49118 / 3.06114 / 0.43004, grad norm = 5.7397, 667 model + 62 RLT tensors saved and finite;
- formal Stage 2 semantics use **C=10**, reference horizon **H=50**, reference dropout **0.5**; mock sub-step / early-done timing tests pass, real rollout is still pending;
- next main gate: **2,000-step Stage 1 joint-full → Stage 2 feature-load check → real C=10 Stage 2 smoke**;
- detailed daily record: [`research/progress-2026-09-12.md`](research/progress-2026-09-12.md).

### Phase 1 — Failure Diagnosis
Determine whether failures come from observability, action candidates, critic/value learning, data coverage, or execution horizon.

### Phase 2 — Physical Experience Representation
Only after diagnosis, investigate action consequence, value-oriented physics, execution history, correction benefit, etc.

### Phase 3 — Self-Improvement Loop
Study repeated Deploy → Experience → Learn → Redeploy cycles, retention, consolidation and experience reuse.

## Platform split

- **RoboTwin 2.0 / RLinf_support**: current pinned baseline reproduction path.
- **RoboTwin 2.0 main**: migration / modern-environment comparison after the first baseline is frozen.
- **RoboDojo on B300**: daily side track for hardware compatibility, install / renderer smoke, XPolicyLab debug and Dojo-Eval bring-up. No B300 simulator-compatibility conclusion is recorded until it is actually tested.

## Research north star

> How can a robot turn one physical experience into a better next action — and eventually accumulate, consolidate and reuse that experience across tasks and embodiments?

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
    ├── master-roadmap.md
    ├── rlt-multitask-benchmark.md
    ├── progress-2026-09-12.md
    ├── robodojo-b300-log.md
    ├── experiment-log.md
    ├── decision-log.md
    ├── frontier-landscape.md
    ├── perspectives-and-theses.md
    └── reading-program.md
```

## Maintenance rule

New papers do **not** automatically change the project mainline.

They first update:
- innovation boundaries,
- baseline / ablation choices,
- diagnosis hypotheses,
- long-term research map.

The mainline changes only when experiments or strong neighboring evidence justify it.

## Knowledge-base architecture

The live site intentionally separates:

- **Project Mainline** — current phase, experiments, evidence and next actions.
- **Frontier Knowledge Base** — papers, systems, labs, research directions, boundaries and inspiration.
- **Historical Archive** — immutable previous Research OS snapshots.

Key files:

- `data/frontier.json` — searchable frontier-work database.
- `research/frontier-landscape.md` — detailed “what others are doing” survey.
- `research/perspectives-and-theses.md` — external RSI viewpoints and long-term synthesis.
- `research/reading-program.md` — daily reading tracks.
- `research/knowledge-base-maintenance.md` — update protocol.
- `archive/v0.4-original.html` — preserved full v0.4 snapshot.

The website is intended to be the project's **first research entry point and decision memory**, not the only source of truth. New public work still needs continuous search, verification and ingestion.
