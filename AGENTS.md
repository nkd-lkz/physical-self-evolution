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

## Publish project updates through the research homepage

For RLT project research, idea and daily development updates, treat `index.html`
as the canonical user-facing entry. Reuse existing topic notes or daily reports;
do not create competing overview files. Update `data/current-status.json` for the
latest evidence and priorities, and append/prepend actual dated progress to
`data/experiments.json`. Preserve historical snapshots rather than silently
rewriting their outcomes. Never invent a daily development result.

`data/research-hub.json` maintains the small set of featured readings and research
hypotheses (implementation, controls, decision gates). Detailed project Markdown
in `research/` and `notes/` is automatically indexed. Run
`python research/scripts/build_site_index.py` after editing project notes; Pages
rebuilds the same index on deployment. Existing publication metadata in
`data/papers.json`, `latest-readings.json`, `frontier*.json` and the reading ledger
remains the source for paper status and provenance. Keep the separate survey
routing rules above; this homepage index never scans `survey-rsi/`.
