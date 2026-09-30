"""Build compact evidence JSON and vector figures from completed diagnostics."""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
COLORS = {
    "ink": "#172B4D",
    "blue": "#2878B5",
    "teal": "#168B81",
    "orange": "#D77A28",
    "gray": "#66758A",
    "pale": "#F3F6FA",
}
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.labelcolor": COLORS["ink"],
        "text.color": COLORS["ink"],
    }
)


def read(path):
    return json.loads(path.read_text())


def export(fig, stem):
    for extension in ("svg", "pdf", "png"):
        target = stem.with_suffix("." + extension)
        fig.savefig(
            target,
            dpi=240,
            bbox_inches="tight",
            facecolor="white",
        )
        if extension == "svg":
            target.write_text(
                "\n".join(line.rstrip() for line in target.read_text().splitlines())
                + "\n"
            )
    plt.close(fig)


def block(ax, x, y, title, detail, color="blue", width=2.65):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            width,
            1.05,
            boxstyle="round,pad=0.04,rounding_size=0.09",
            linewidth=1.3,
            edgecolor=COLORS[color],
            facecolor="white",
        )
    )
    ax.text(
        x + width / 2,
        y + 0.72,
        title,
        ha="center",
        va="center",
        fontsize=11,
        weight="bold",
        color=COLORS[color],
    )
    ax.text(
        x + width / 2,
        y + 0.3,
        detail,
        ha="center",
        va="center",
        fontsize=8.4,
        linespacing=1.4,
    )


def arrow(ax, start, end, label="", learning=False, label_dx=0):
    color = COLORS["orange" if learning else "gray"]
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=1.25,
            linestyle="--" if learning else "-",
            color=color,
        )
    )
    if label:
        ax.text(
            (start[0] + end[0]) / 2 + label_dx,
            (start[1] + end[1]) / 2 + 0.15,
            label,
            ha="center",
            fontsize=8.2,
            color=color,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.3},
        )


def architecture(name, output):
    titles = {
        "flare": "A   Learn a consequence-sensitive state",
        "zeva": "B   Reuse completed interaction evidence",
        "jev": "C   Learn which bounded correction to execute",
    }
    fig, ax = plt.subplots(figsize=(13.6, 5.9))
    ax.set(xlim=(0, 13.8), ylim=(-0.3, 6.0))
    ax.axis("off")
    ax.text(0.25, 5.72, titles[name], fontsize=18, weight="bold")
    ax.text(
        0.25,
        5.34,
        "RLT research prototype  |  Same frozen VLA / reference  |  Separate, unmerged experiments",
        color=COLORS["gray"],
        fontsize=9,
    )
    block(ax, 0.3, 3.8, "Observation", "Images + instruction\nJoint state")
    block(
        ax,
        3.7,
        3.8,
        "Frozen Stage 1",
        "VLA + RLT encoder\nState token z; reference chunk",
        "gray",
    )
    arrow(ax, (3.02, 4.3), (3.62, 4.3))
    if name == "flare":
        block(
            ax,
            7.1,
            3.8,
            "State adapter",
            "e = E(z, q), 128 dimensions\nLearned from TD + future loss",
            "teal",
        )
        block(
            ax,
            10.5,
            3.8,
            "RLT actor / critic",
            "Actor reads detached e\nExecute through baseline routing",
        )
        arrow(ax, (6.4, 4.3), (7.02, 4.3))
        arrow(ax, (9.8, 4.3), (10.42, 4.3))
        block(
            ax,
            3.7,
            1.35,
            "Completed transition",
            "Actual action prefix + successor\nFrozen future token; stop gradient",
            "gray",
        )
        block(
            ax,
            7.1,
            1.35,
            "Future predictor",
            "[e, action prefix, query]\nLatent residual + proprio change",
            "teal",
        )
        block(
            ax,
            10.5,
            1.35,
            "Environment / replay",
            "Real executed actions only\nTerminal dynamics targets masked",
        )
        arrow(ax, (11.82, 3.72), (11.82, 2.48), "execute")
        arrow(ax, (11.82, 1.28), (11.82, 0.97))
        arrow(ax, (11.82, 0.97), (5.05, 0.97), "record")
        arrow(ax, (5.05, 0.97), (5.05, 1.29))
        arrow(ax, (8.4, 3.72), (8.4, 2.48), "e + actions", label_dx=0.35)
        arrow(ax, (6.4, 2.05), (7.02, 2.05), "target")
        arrow(
            ax, (7.55, 2.48), (7.55, 3.72), "future loss", learning=True, label_dx=-0.35
        )
        message = "No pixel generation. Predicted futures are auxiliary supervision, not the default online planner."
    elif name == "zeva":
        block(
            ax,
            7.1,
            3.8,
            "Memory context",
            "Attention reader (64D)\nor fixed response features",
            "teal",
        )
        block(
            ax,
            10.5,
            3.8,
            "RLT actor / critic",
            "Current state + memory context\nTD for reader; actor detaches",
        )
        arrow(ax, (6.4, 4.3), (7.02, 4.3))
        arrow(ax, (9.8, 4.3), (10.42, 4.3))
        block(
            ax,
            3.7,
            1.35,
            "Evidence snapshot",
            "4 recent + 4 retrieved records\nReplay never backfills old context",
            "gray",
        )
        block(
            ax,
            7.1,
            1.35,
            "Interaction archive",
            "Start q, executed u, actual delta q\nOnly completed prefixes",
            "teal",
        )
        block(
            ax,
            10.5,
            1.35,
            "Environment feedback",
            "True terminal state before reset\nPer-environment isolation",
        )
        arrow(ax, (11.82, 3.72), (11.82, 2.48), "execute")
        arrow(ax, (10.42, 1.85), (9.83, 1.85))
        arrow(ax, (7.02, 1.85), (6.43, 1.85))
        arrow(ax, (5.05, 2.48), (7.7, 3.72), "past-only read")
        message = "Joint response is evidence, not a contact label. Default reset clears memory; long-term growth is unproven."
    else:
        block(
            ax,
            7.1,
            3.8,
            "Finite candidate bank",
            "Reference + bounded joint edits\nUp to 17; gripper inherited",
            "teal",
        )
        block(
            ax,
            10.5,
            3.8,
            "Local selector",
            "Scores bounded candidates\nChooses ONE complete chunk",
            "teal",
        )
        arrow(ax, (6.4, 4.3), (7.02, 4.3))
        arrow(ax, (9.8, 4.3), (10.42, 4.3))
        block(
            ax,
            3.7,
            1.35,
            "Executed replay",
            "Store actions, not choice IDs\nInclude off-vocabulary corrections",
            "gray",
        )
        block(
            ax,
            7.1,
            1.35,
            "Continuous twin critic",
            "TD from actual transitions\nScore candidates for policy update",
        )
        block(
            ax,
            10.5,
            1.35,
            "Environment / routing",
            "Same reward and takeover rules\nNo simulated candidate previews",
        )
        arrow(ax, (11.82, 3.72), (11.82, 2.48), "execute")
        arrow(ax, (6.42, 1.85), (7.03, 1.85), "TD")
        arrow(ax, (9.0, 2.48), (11.0, 3.72), "distill soft improvement", learning=True)
        arrow(ax, (11.82, 1.28), (11.82, 0.97))
        arrow(ax, (11.82, 0.97), (5.05, 0.97), "record actual outcome")
        arrow(ax, (5.05, 0.97), (5.05, 1.29))
        message = "Inspired by typed decisions, not a Jev API integration. Bounded joint corrections are not learned skills."
    ax.text(0.3, 0.55, message, fontsize=10)
    ax.text(
        0.3,
        0.02,
        "Solid: data flow    Dashed orange: learning signal    Scope: prototype mechanism, not established robot improvement",
        fontsize=8.5,
        color=COLORS["gray"],
    )
    export(fig, output / f"{name}-architecture")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_root", type=Path)
    args = parser.parse_args()
    root = args.run_root
    figures = ROOT / "research/figures/three-branch-audit-2026-09-30"
    figures.mkdir(parents=True, exist_ok=True)
    data = {
        "as_of": "2026-09-30",
        "scope": "Development diagnostics, not robot success or transfer evidence",
        "run": root.name,
        "runs": {},
    }
    for task in ("flare", "zeva", "jev", "jev_mixed", "jev_warmup"):
        path = root / task / "models/results.json"
        manifest = read(root / task / "manifest.json")
        if manifest["status"] != "completed":
            raise RuntimeError(f"{task} has not completed")
        results = read(path)
        # Do not publish full NAS paths or thousands of unrelated source hashes.
        for row in results["results"]:
            row.pop("checkpoint", None)
        if "data" in results:
            results["data"] = {
                k: v
                for k, v in results["data"].items()
                if k not in ("gpu_uuid", "renderer")
            }
        data["runs"][task] = {
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "manifest": {
                k: manifest[k]
                for k in (
                    "git_revision",
                    "tracked_diff_sha256",
                    "torch",
                    "seconds",
                    "device",
                    "max_reserved_mib",
                    "max_allocated_mib",
                )
                if k in manifest
            },
            "results": results,
        }
    data["zeva_empirical_test_mse"] = read(root / "zeva/empirical/results.json")[
        "results"
    ]["test"]["mse"]
    for task in ("flare", "zeva", "jev"):
        path = root / f"{task}_fsdp/models/results.json"
        if path.exists():
            result = read(path)
            data["runs"][f"{task}_fsdp"] = {
                "scope": result["scope"],
                "checkpoint_action_parity": result["checkpoint_action_parity"],
                "updated_tensors": sum(
                    v > 0 for v in result["parameter_max_delta"].values()
                ),
                "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        architecture(task, figures)
    target = ROOT / "data/three-branch-audit-2026-09-30.json"
    target.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    )
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    colors = [COLORS[k] for k in ("gray", "blue", "teal", "orange")]
    flare = data["runs"]["flare"]["results"]["results"]
    for mode, label, color in zip(
        ("direct", "residual", "action_free"),
        ("Direct", "Residual + actions", "Residual, no actions"),
        colors[1:],
    ):
        values = np.array(
            [
                [r["horizons"][str(h)]["cosine_error"] for h in (1, 5, 10)]
                for r in flare
                if r["mode"] == mode
            ]
        )
        axes[0].errorbar(
            [1, 5, 10],
            values.mean(0),
            yerr=values.std(0, ddof=1),
            marker="o",
            capsize=3,
            label=label,
            color=color,
        )
    axes[0].plot(
        [1, 5, 10],
        [flare[0]["horizons"][str(h)]["persistence_cosine_error"] for h in (1, 5, 10)],
        "--",
        color=colors[0],
        label="Persistence",
    )
    axes[0].set(
        title="A  Frozen-feature prediction",
        xlabel="Future control horizon",
        ylabel="Cosine error (lower is better)",
        xticks=[1, 5, 10],
    )
    axes[0].legend(fontsize=8)
    zeva = data["runs"]["zeva"]["results"]["results"]
    labels = ["None", "Recent", "Archive", "Full", "Response", "Formula"]
    means, deviations = [], []
    for mode in ("none", "recent", "archive", "full", "response"):
        values = [r["test"]["mse"] * 1e4 for r in zeva if r["mode"] == mode]
        means.append(np.mean(values))
        deviations.append(np.std(values, ddof=1))
    means.append(data["zeva_empirical_test_mse"] * 1e4)
    deviations.append(0)
    axes[1].bar(
        labels,
        means,
        yerr=deviations,
        color=[colors[0]] * 4 + [colors[2], colors[3]],
        capsize=3,
    )
    axes[1].set(
        title="B  Hidden-drive response probe",
        ylabel="Joint-change MSE x 10,000 (lower)",
    )
    axes[1].tick_params(axis="x", rotation=30)
    for mode, color in (("atomic", colors[2]), ("continuous", colors[1])):
        rows = data["runs"]["jev_warmup"]["results"]["results"]
        vals = np.array(
            [[v["mean_reward"] for v in r["curve"]] for r in rows if r["mode"] == mode]
        )
        x = [v["step"] for v in rows[0]["curve"]]
        axes[2].plot(x, vals.mean(0), label=mode.capitalize(), color=color)
        axes[2].fill_between(
            x,
            vals.mean(0) - vals.std(0, ddof=1),
            vals.mean(0) + vals.std(0, ddof=1),
            color=color,
            alpha=0.15,
        )
    axes[2].axvline(300, color=colors[0], linestyle=":", linewidth=1)
    axes[2].set(
        title="C  Synthetic critic/actor stress test",
        xlabel="Critic updates (actor begins at 300)",
        ylabel="Executed-action reward (higher)",
    )
    axes[2].legend(fontsize=8)
    for ax in axes:
        ax.grid(axis="y", alpha=0.15)
    fig.suptitle(
        "Mechanism diagnostics are not robot success rates", fontsize=16, weight="bold"
    )
    fig.text(
        0.5,
        -0.01,
        "Three initialization seeds; bands/bars = sample SD, not confidence intervals. Reused development data. C: mixed data, actor LR 1e-4; both share identical transitions.",
        ha="center",
        fontsize=8,
    )
    fig.tight_layout()
    export(fig, figures / "diagnostic-results")
    print(f"Published {target} and {figures}")


if __name__ == "__main__":
    main()
