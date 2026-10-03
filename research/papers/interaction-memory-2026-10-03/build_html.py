"""Create an accessible HTML companion from the compiled manuscript source."""
from pathlib import Path
import re

from bs4 import BeautifulSoup
import pypandoc

ROOT = Path(__file__).resolve().parent
source = (ROOT / "paper_en.tex").read_text()
aux = (ROOT / "paper_en.aux").read_text()
numbers = dict(re.findall(r"\\newlabel\{([^}]+)\}\{\{([^}]+)\}", aux))


def table_for_pandoc(match):
    body = match[1]
    first_row = next(line for line in body.splitlines() if "&" in line)
    return "\\begin{tabular}{" + "l" * (first_row.count("&") + 1) + "}\n" + body + "\\end{tabular}"


# Pandoc does not interpret the custom tabularx column type or algorithmicx.
text = re.sub(r"\\begin\{tabularx\}[^\n]*\n(.*?)\\end\{tabularx\}",
              table_for_pandoc, source, flags=re.S)
text = text.replace("figures/framework.pdf", "figures/framework.svg")
text = text.replace("figures/pilot_diagnostics.pdf", "figures/pilot_diagnostics.svg")
algorithm = re.search(r"\\begin\{algorithm\}.*?\\end\{algorithm\}", text, re.S)[0]
requirement = re.search(r"\\Require ([^\n]+)", algorithm)[1]
items = []
for line in algorithm.splitlines():
    line = line.strip()
    if line.startswith("\\State "):
        items.append("\\item " + line[7:])
    elif line.startswith("\\For{"):
        items.append("\\item \\textbf{For " + line[5:])
    elif line.startswith("\\If{"):
        items.append("\\item \\textbf{If " + line[4:])
replacement = ("\\begin{quote}\n\\textbf{Algorithm 1. IM-RLT online learning with a fixed context representation (proposed)}\n"
               "\\label{alg:online}\n\\textbf{Input:} " + requirement +
               "\n\\begin{enumerate}\n" + "\n".join(items) + "\n\\end{enumerate}\n\\end{quote}")
text = text.replace(algorithm, replacement)
html = pypandoc.convert_text(text, "html5", format="latex", extra_args=[
    "--standalone", "--mathml", "--citeproc", "--bibliography=" + str(ROOT / "references.bib"),
    "--csl=" + str(ROOT / "bibliography_style.csl"), "--number-sections",
    "--css=document.css", "--metadata=lang:en"])
soup = BeautifulSoup(html, "html.parser")
soup.body["class"] = ["manuscript"]
# Match equation/algorithm references to the actual compiled PDF numbering.
for link in soup.select("a[data-reference]"):
    label = link["data-reference"]
    if label not in numbers:
        raise ValueError(f"Unresolved source reference: {label}")
    link.string = numbers[label]
for math in soup.find_all("math", attrs={"display": "block"}):
    annotation = math.find("annotation")
    labels = re.findall(r"\\label\{([^}]+)\}", annotation.get_text() if annotation else "")
    wrapper = soup.new_tag("div", attrs={"class": "display-equation"})
    math.wrap(wrapper)
    for label in labels:
        anchor = soup.new_tag("span", id=label)
        wrapper.insert(0, anchor)
    if labels:
        number = soup.new_tag("span", attrs={"class": "equation-number"})
        number.string = "(" + ", ".join(numbers[label] for label in labels) + ")"
        wrapper.append(number)
tables = re.findall(r"\\begin\{table\}.*?\\end\{table\}", source, re.S)
assert len(soup.find_all("table")) == len(tables), "A source table was lost"
for table, block in zip(soup.find_all("table"), tables):
    label = re.search(r"\\label\{([^}]+)\}", block)[1]
    existing = soup.find(id=label)
    if existing is not None:
        del existing["id"]
    table["id"] = label
    table.caption.insert(0, "Table " + numbers[label] + ". ")
for figure in soup.find_all("figure"):
    label = figure.get("id")
    if label in numbers and figure.figcaption:
        figure.figcaption.insert(0, "Figure " + numbers[label] + ". ")
for block in soup.find_all("blockquote"):
    if "Algorithm 1." in block.get_text():
        existing = soup.find(id="alg:online")
        if existing is not None:
            del existing["id"]
        block["id"] = "alg:online"
        block["class"] = ["algorithm"]
# The LaTeX appendix marker is not numbered alphabetically by Pandoc.
in_appendix = False
appendix = 0
for heading in soup.find_all(["h1", "h2", "h3"]):
    if heading.get("id", "").startswith("app:") and heading.name == "h1":
        in_appendix = True
        appendix += 1
    if in_appendix and heading.find(class_="header-section-number"):
        n = heading.find(class_="header-section-number")
        original = n.get_text().split(".")
        n.string = chr(64 + appendix) + ("." + ".".join(original[1:]) if len(original) > 1 else "")
# Put the bibliography before the appendices, as in the PDF.
refs = soup.find(id="refs")
ref_heading = soup.new_tag("h1", id="references")
ref_heading.string = "References"
appendix_heading = soup.find(id="app:implementation")
appendix_heading.insert_before(ref_heading)
appendix_heading.insert_before(refs.extract())
nav = BeautifulSoup('<nav><a href="../../../index.html">科研工作台</a> · <a href="paper_en.pdf">Typeset PDF · v2</a> · <a href="paper_en.tex">LaTeX source</a> · <a href="experiment_guide_zh.html">中文实验指南</a> · <a href="index.html">All downloads</a></nav>', "html.parser").nav
soup.body.insert(0, nav)
note = soup.new_tag("p", attrs={"class": "publication-note"})
note.string = "Version 2 · 3 October 2026. Proposed method with measured development diagnostics; controlled online-RL and transfer results remain pending. The PDF is the reference layout; this HTML uses the same manuscript source and native MathML."
soup.find(id="title-block-header").insert_after(note)
ids = {item["id"] for item in soup.find_all(id=True)}
assert len(ids) == len(soup.find_all(id=True)), "Duplicate HTML anchors"
missing = [a["href"] for a in soup.select('a[href^="#"]') if a["href"][1:] not in ids]
assert not missing, f"Unresolved HTML anchors: {missing}"
assert len(soup.select(".csl-entry")) == 26
(ROOT / "paper_en.html").write_text(str(soup), encoding="utf-8")
print("HTML: 7 tables, 2 figures, 26 references; all internal anchors resolved")
