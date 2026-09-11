# Physical Self-Evolution

Living research website for **Physical Interaction, Embodied Self-Evolution, VLA, Online RL, Memory / ICL, WAM, Failure Recovery and robot learning experiments**.

## Website

After GitHub Pages is enabled, the site will be available at:

**https://nkd-lkz.github.io/physical-self-evolution/**

## Research north star

> How can a robot turn one physical experience into a better next action — and eventually accumulate, consolidate and reuse that experience across tasks and embodiments?

Current project strategy:

**RLT baseline → failure diagnosis → evidence-driven algorithm iteration → multi-task / OOD → self-improvement loop**

## Repository structure

```
.
├── index.html
├── reader.html
├── assets/
│   ├── style.css
│   └── app.js
├── data/
│   ├── papers.json
│   ├── experiments.json
│   └── decisions.json
├── notes/
│   ├── zeva.md
│   ├── rlt.md
│   └── smoothrl.md
├── research/
│   ├── master-roadmap.md
│   ├── experiment-log.md
│   └── decision-log.md
└── .github/workflows/pages.yml
```

## Maintenance rule

New papers do **not** automatically change the research direction.

They are first used to update:
- innovation boundary,
- baseline / ablation choices,
- diagnosis hypotheses,
- long-term research map.

The mainline changes only when experiments or strong neighboring evidence justify it.
