# Physical Self-Evolution

Living research website for **Physical Interaction, Embodied Self-Evolution, VLA, Online RL, Memory / ICL, Failure Recovery and robot learning experiments**.

## Website

**https://nkd-lkz.github.io/physical-self-evolution/**

## Current research phase

### Phase 0 — RLT Multi-task Benchmark **← current**
Build a reproducible multi-task VLA + Online RL research bench on RoboTwin2.

### Phase 1 — Failure Diagnosis
Determine whether failures come from observability, action candidates, critic/value learning, data coverage, or execution horizon.

### Phase 2 — Physical Experience Representation
Only after diagnosis, investigate action consequence, value-oriented physics, execution history, correction benefit, etc.

### Phase 3 — Self-Improvement Loop
Study repeated Deploy → Experience → Learn → Redeploy cycles, retention, consolidation and experience reuse.

## Platform split

- **RoboTwin2**: main algorithm-development track.
- **RoboDojo on B300**: daily side track for installation, compatibility, smoke test and Dojo-Eval bring-up.

## Research north star

> How can a robot turn one physical experience into a better next action — and eventually accumulate, consolidate and reuse that experience across tasks and embodiments?

## Repository structure

\`\`\`
.
├── index.html
├── reader.html
├── assets/
├── data/
├── notes/
└── research/
    ├── master-roadmap.md
    ├── rlt-multitask-benchmark.md
    ├── robodojo-b300-log.md
    ├── experiment-log.md
    └── decision-log.md
\`\`\`

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

- \`data/frontier.json\` — searchable frontier-work database.
- \`research/frontier-landscape.md\` — detailed “what others are doing” survey.
- \`research/perspectives-and-theses.md\` — external RSI viewpoints and long-term synthesis.
- \`research/reading-program.md\` — daily reading tracks.
- \`research/knowledge-base-maintenance.md\` — update protocol.
- \`archive/v0.4-original.html\` — preserved full v0.4 snapshot.

The website is intended to be the project's **first research entry point and decision memory**, not the only source of truth. New public work still needs continuous search, verification and ingestion.
