"""Stage only the RLT project website. survey-rsi stays a separate GitHub library."""
from pathlib import Path
import argparse
import shutil

ROOT = Path(__file__).resolve().parents[2]
ENTRIES = ("index.html", "reader.html", "README.md", ".nojekyll",
           "assets", "data", "notes", "research", "archive")

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('output', type=Path)
args = parser.parse_args()
output = args.output.resolve()
if output.exists():
    raise SystemExit('Choose a new staging directory; existing contents are not removed.')
if output == ROOT or ROOT in output.parents:
    raise SystemExit('Stage outside the repository.')
output.mkdir(parents=True)
for name in ENTRIES:
    src, dest = ROOT/name, output/name
    if src.is_dir():
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    else:
        shutil.copy2(src, dest)
assert not (output/'survey-rsi').exists()
print('RLT site staged; survey-rsi is not included.')
