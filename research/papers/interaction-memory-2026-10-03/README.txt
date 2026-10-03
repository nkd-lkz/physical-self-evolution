RLT interaction-memory research bundle — 2026-10-03

Start with index.html, paper_en.pdf, or experiment_guide_zh.pdf.
English: extended research manuscript; Chinese: experiment execution guide.
This is a proposed method with separately labeled development observations.
No new algorithm training or controlled success/transfer claim is supplied.

Editable sources: paper_en.tex and both HTML files.
PDFs were rendered from HTML; the LaTeX source has NOT been compiled locally.
The LaTeX source is a standalone article, not the CVPR 2027 review template.
Use the current official CVPR template after results and scope are frozen.
All figures are supplied as SVG, PDF, and PNG, with equation SVGs for HTML.
references.bib contains 25 verified primary-paper entries.
references.json records arXiv metadata checked on 2026-10-03.
evidence_manifest.json records original measured files, hashes, and recomputed means.
experiment_matrix.csv is a planned matrix, not a runnable launcher.
upstream_commits.json and upstream_prs.json are read-only check snapshots.

PDF regeneration requires WeasyPrint 70.0 and suitable fonts (Droid Sans Fallback
for Chinese). Use a separate document environment; do not change the RL venv:
    python build_pdf.py

Checks: primary bibliography metadata; measured MSE means; relative asset links;
PDF text/page bounds; visual inspection of framework and selected PDF pages;
read-only baseline GPU-0 and attention GPU-1 launcher preflights passed.
No new GPU training was launched. The preflight does not test GPU execution.
No remote research/upstream merge was performed.

Public release revision, 2026-10-03:
Baseline acceptance now precedes Stage 1B development. The Chinese guide
sections 4, 11 and 13 were updated; the manuscript includes a publication note.
Internal filesystem locations were removed from the evidence manifest and guide.
The raw-evidence hashes remain unchanged; raw artifacts are not included.
HTML and PDFs contain the same public update. No new GPU experiment is claimed.
