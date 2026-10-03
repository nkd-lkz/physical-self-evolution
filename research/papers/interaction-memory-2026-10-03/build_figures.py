"""Rebuild the proposed architecture and measured diagnostics from public data."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figures"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none"})
BLUE, PURPLE, GREEN, GRAY = "#e8f0fa", "#eee7f6", "#e2f1eb", "#f0f2f4"
INK = "#243347"


def save(fig, name):
    for suffix in ("pdf", "svg", "png"):
        fig.savefig(OUT / f"{name}.{suffix}", bbox_inches="tight", dpi=220)
    svg = OUT / f"{name}.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    plt.close(fig)


fig, ax = plt.subplots(figsize=(10.8, 5.3))
ax.set(xlim=(0, 10.8), ylim=(0, 5.3))
ax.axis("off")


def box(x, y, w, h, label, color=GRAY, size=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.035,rounding_size=0.06",
                              linewidth=0.9, edgecolor="#7b8795", facecolor=color))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=size, color=INK)


def arrow(start, end, dashed=False, color=INK):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=12,
                                linewidth=1.0, linestyle="--" if dashed else "-", color=color))


ax.text(0, 5.12, "(a) Stage 1B: learn a context that predicts a later response", weight="bold", fontsize=12)
box(0.02, 3.96, 1.68, 0.77, "Earlier completed\ncommand–response\nevents: i < t", size=9.5)
box(2.0, 3.96, 1.32, 0.77, "Event encoder\nE", PURPLE)
box(3.62, 3.96, 2.1, 0.77, "Recent 4 + archive 32\nRetrieve 4; reader R", PURPLE)
box(6.02, 3.96, 1.5, 0.77, "Context c\n64 dimensions", PURPLE)
box(7.82, 3.96, 1.3, 0.77, "Consequence\ndecoder F", PURPLE)
for a, b in [(1.72, 1.97), (3.34, 3.59), (5.74, 5.99), (7.54, 7.79)]:
    arrow((a, 4.345), (b, 4.345))
box(3.62, 2.97, 2.1, 0.57, "Current frozen state", BLUE, 9.8)
box(6.02, 2.97, 1.5, 0.57, "Command to predict", GRAY, 8.8)
arrow((4.67, 3.56), (4.67, 3.94))
ax.plot([6.77, 6.77, 8.47], [3.56, 3.75, 3.75], color=INK, lw=0.9)
arrow((8.47, 3.75), (8.47, 3.94))
box(9.46, 3.96, 1.29, 0.77, "Observed\nfuture targets", BLUE, 9.2)
arrow((9.44, 4.345), (9.14, 4.345), dashed=True, color="#775297")
ax.text(9.78, 3.36, "Joint + visual\nconsequence loss", ha="center", fontsize=9, color="#775297")
ax.text(0.02, 3.23, "Train E, R, F.\nKeep VLA/token fixed.", fontsize=10, color=INK)
ax.plot([0, 10.8], [2.75, 2.75], color="#d0d6df", lw=0.8)

ax.text(0, 2.47, "(b) Stage 2: fixed representation, small actor–critic updates", weight="bold", fontsize=12)
box(0.02, 1.38, 2.12, 0.77, "Current observation\nFrozen VLA + RL token\nState + reference", BLUE, 9.5)
box(2.5, 1.38, 2.0, 0.77, "Earlier memory\nFrozen E + R\nContext c", BLUE, 9.5)
box(4.87, 1.38, 1.83, 0.77, "Small actor + critics\nMatched RL losses", GREEN, 9.5)
box(7.06, 1.38, 1.68, 0.77, "Baseline routing\nCommitted chunk", GRAY, 9.5)
box(9.1, 1.38, 1.64, 0.77, "Environment\nReal successor", GRAY, 9.5)
arrow((2.16, 1.765), (2.47, 1.765))
arrow((4.52, 1.765), (4.84, 1.765))
arrow((6.72, 1.765), (7.03, 1.765))
arrow((8.76, 1.765), (9.07, 1.765))
ax.text(6.88, 2.21, "actor", fontsize=8.5, ha="center", color=INK)
# The baseline state and reference also reach the controller directly.
ax.plot([1.08, 1.08, 5.78], [1.34, 1.02, 1.02], color=INK, lw=0.9)
arrow((5.78, 1.02), (5.78, 1.36))
ax.text(1.75, 0.81, "current state + reference", ha="center", fontsize=9, color=INK)
# Only after completion can a new event enter the next decision's memory.
ax.plot([9.92, 9.92, 3.5], [1.34, 0.24, 0.24], color="#506c89", lw=1.0)
arrow((3.5, 0.24), (3.5, 1.36), color="#506c89")
ax.text(6.65, 0.43, "Append completed event for the next decision; snapshot replay", ha="center", fontsize=9, color="#506c89")
save(fig, "framework")

metrics = json.loads((ROOT / "evidence_manifest.json").read_text())["metrics"]
fig, axes = plt.subplots(1, 2, figsize=(10.7, 3.9), gridspec_kw={"width_ratios": [1.2, 1]})
keys = ["none", "recent", "archive", "full", "response", "fixed_formula"]
names = ["No history", "Recent", "Archive", "Full attention", "Response + head", "Fixed formula"]
means = [metrics[k].get("mean_mse", metrics[k].get("mse")) * 1e4 for k in keys]
stds = [np.std(metrics[k]["per_seed_mse"], ddof=1) * 1e4 if "per_seed_mse" in metrics[k] else 0 for k in keys]
ax = axes[0]
ax.barh(names, means, xerr=stds, color=["#aebac8"] * 4 + ["#947caf", "#468671"], capsize=3, height=0.62)
ax.invert_yaxis()
ax.set_xlim(0, 2.24)
for i, value in enumerate(means):
    ax.text(value + 0.055, i, f"{value:.3f}", va="center", fontsize=8.5)
ax.set_title("(a) Initial response probes", loc="left", fontsize=11, weight="bold")
ax.set_xlabel("Joint-response MSE (×10⁻⁴), lower is better")
ax = axes[1]
keys = ["fixed_formula", "response_residual", "response_supported"]
overall = [metrics[k].get("mean_mse", metrics[k].get("mse")) * 1e4 for k in keys]
late = [metrics[k].get("mean_late_mse", metrics[k].get("late_mse")) * 1e4 for k in keys]
x = np.arange(3)
ax.bar(x - 0.17, overall, width=0.32, label="All windows", color="#667d9c")
ax.bar(x + 0.17, late, width=0.32, label="Late history", color="#c4d6cb")
ax.set_xticks(x, ["Fixed\nformula", "+ Learned\nresidual", "+ Support-gated\nresidual"])
ax.set_ylim(0, 0.96)
for i, (a, b) in enumerate(zip(overall, late)):
    ax.text(i - 0.17, a + 0.016, f"{a:.3f}", ha="center", fontsize=8)
    ax.text(i + 0.17, b + 0.016, f"{b:.3f}", ha="center", fontsize=8)
ax.set_title("(b) Post-hoc residual study", loc="left", fontsize=11, weight="bold")
ax.set_ylabel("Joint-response MSE (×10⁻⁴)")
ax.legend(frameon=False, fontsize=9, loc="upper right")
for ax in axes:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x" if ax is axes[0] else "y", color="#dfe4e9", linewidth=0.6)
    ax.set_axisbelow(True)
fig.tight_layout(w_pad=2.2)
save(fig, "pilot_diagnostics")
