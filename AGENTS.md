# Route the task before reading project content

This repository has two separate knowledge domains. Do not load both as default context.

## RSI survey tasks

For literature review, daily RSI research, paper cards or survey writing, read only
`survey-rsi/AGENTS.md`, `survey-rsi/MAINTENANCE.md`, `survey-rsi/SCOPE.md` and other
files inside `survey-rsi/`, plus public primary external sources. Do not read the
root README, website, root data, research notes, experimental code or project
conversation history to inform the survey. Git metadata and boundary checks are
allowed. Write only to `survey-rsi/`; do not maintain the root entry during daily runs.

## RLT / Physical Token tasks

Project tasks may read `research/`, `notes/`, root `data/` and the website. They may
also cite public paper cards from `survey-rsi/`. Keep project hypotheses, experiment
designs, implementation decisions and progress in the project area. Never write
them into the survey, including as paraphrased "survey implications".

Publicly published RLT-related papers are normal external literature; cite their
original publication rather than this repository's project notes.

## Explicit cross-domain maintenance

Only an explicit user request to reorganize/isolate the domains authorizes a
cross-domain migration. Preserve project material in its own area; survey pages
must not link back to project material or retain project excerpts in logs.
Run `python survey-rsi/scripts/check_boundary.py` before committing. This is a
content-routing safeguard, not access control or a guarantee about Git history.
