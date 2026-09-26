# This directory: embodied/robot RSI survey literature

Read README.md, MAINTENANCE.md and SCOPE.md before updating. Keep paper cards in Chinese, use full titles rather than arbitrary numbered IDs. Use primary sources and record exact paper versions and evidence locations. Do not claim reproduction.

Deduplicate against data/baseline.json and data/catalog.json using arXiv IDs without version, DOI, normalized full title and author/project metadata. Keep abstract-only candidates separate. Preserve historical daily logs and human edits.

Read and write only survey-rsi/ plus public primary external sources; necessary Git metadata is allowed. Do not read the root README, project research/notes/data, website, experiments or project conversation context to inform this survey. Do not maintain the root entry during daily runs. Never import project hypotheses, design choices, progress, private conversation screenshots or internal context, even as paraphrased survey implications. Do not add project backlinks or redirects. Other project areas may cite the survey's public literature; the reverse flow is prohibited. Publicly published RLT-related papers remain eligible, sourced to their original publications.

New papers, corrected evidence and no-update outcomes all need honest daily logs. Source figures must be attributed. Run python survey-rsi/scripts/check_boundary.py before committing. Historical logs must not preserve cross-domain content after a user-authorized boundary correction; keep their public-literature counts and a brief correction note instead.
