IM-RLT manuscript bundle — version 2, 2026-10-03

Start with paper_en.pdf (16 pages), paper_en.html, or experiment_guide_zh.pdf.
English: a single-column research manuscript rewritten around the scientific
organization of eRLT and SmoothRL. Chinese: a separate experiment execution guide.
The PDF is compiled from LaTeX. This is not an arXiv posting or a conference template.
The method is proposed; measured tables report existing development diagnostics.
Online control and transfer results remain pending. No new GPU run was performed.

Rebuild in an isolated document environment (not the RL training environment):
  pip install matplotlib numpy pypandoc_binary beautifulsoup4 weasyprint
  python build_figures.py
  python build_pdf.py --tectonic /path/to/tectonic
Validated with Tectonic 0.17.0, Pandoc, and WeasyPrint 70.0.
The first Tectonic run needs network access to obtain its TeX bundle.
Chinese rendering requires a CJK font such as Droid Sans Fallback.
build_pdf.py compiles English TeX, generates HTML, and renders the Chinese guide.
paper_en.bbl is included; references.bib remains the editable bibliography source.
bibliography_style.csl is the upstream IEEE CSL style (license in its header),
used only for HTML citations. This is not an IEEE manuscript template.

Public contents: 2 vector figures (PDF/SVG/PNG), 7 tables in the manuscript,
26 primary-paper references, a planned experiment matrix, evidence hashes,
upstream check snapshots, and build scripts. The HTML uses native MathML.
Some older equation SVG assets remain for historical compatibility; v2 uses
native LaTeX/MathML and does not use those images for equations.

evidence_manifest.json contains aggregate measurements and hashes of private raw
artifacts, not the raw trajectories. It does not establish full reproducibility.
experiment_matrix.csv is a plan, not an executable launcher or measured result.
bundle_checksums.json covers current bundle files except itself and the ZIP.
The v2 ZIP excludes the separate archive and temporary TeX build files.
archive/research_bundle_v1.zip preserves the earlier publication on the website.
