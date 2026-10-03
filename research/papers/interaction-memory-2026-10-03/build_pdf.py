"""Compile the English LaTeX manuscript and render the Chinese HTML guide."""
from pathlib import Path
import argparse
import re
import shutil
import subprocess
import sys
from urllib.parse import urljoin
from weasyprint import HTML

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--tectonic", default="tectonic", help="Path to the Tectonic executable")
args = parser.parse_args()
if not shutil.which(args.tectonic):
    raise SystemExit("Install Tectonic or pass --tectonic /path/to/tectonic")
subprocess.run([args.tectonic, "--keep-logs", "--keep-intermediates", "paper_en.tex"], cwd=root, check=True)
subprocess.run([sys.executable, str(root / "build_html.py")], cwd=root, check=True)
public_base = "https://nkd-lkz.github.io/physical-self-evolution/research/papers/interaction-memory-2026-10-03/"
for stem in ("experiment_guide_zh",):
    content = (root / f"{stem}.html").read_text()
    # PDF links must refer to the published site, never the build filesystem.
    def public_link(match):
        href = match.group(2)
        target = href if href.startswith("#") else urljoin(public_base + stem + ".html", href)
        return match.group(1) + target + match.group(3)
    content = re.sub(r'(<a\b[^>]*\bhref=")([^"]+)(")', public_link, content)
    HTML(string=content, base_url=str(root)).write_pdf(root / f"{stem}.pdf")
