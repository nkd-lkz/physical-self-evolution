"""Render the editable HTML documents to PDF using an isolated document environment."""
from pathlib import Path
import re
from urllib.parse import urljoin
from weasyprint import HTML

root = Path(__file__).resolve().parent
public_base = "https://nkd-lkz.github.io/physical-self-evolution/research/papers/interaction-memory-2026-10-03/"
for stem in ("paper_en", "experiment_guide_zh"):
    content = (root / f"{stem}.html").read_text()
    # PDF links must refer to the published site, never the build filesystem.
    def public_link(match):
        href = match.group(2)
        target = href if href.startswith("#") else urljoin(public_base + stem + ".html", href)
        return match.group(1) + target + match.group(3)
    content = re.sub(r'(<a\b[^>]*\bhref=")([^"]+)(")', public_link, content)
    HTML(string=content, base_url=str(root)).write_pdf(root / f"{stem}.pdf")
