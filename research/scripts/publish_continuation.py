"""Publish completed, predeclared diagnostics without selecting favorable arms."""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from publish_three_branch_audit import COLORS, ROOT, export, plt, read


def collect(root: Path) -> dict:
    """Require the entire matrix and preserve provenance, curves and failures."""
    status = read(root / "status.json")
    if status["status"] != "completed":
        raise ValueError(
            "Publish only a completed matrix; report partial status separately"
        )
    if set(status["completed"]) != {job["name"] for job in status["plan"]}:
        raise ValueError("Completed jobs do not match the declared matrix")
    runs = {}
    for job in status["plan"]:
        directory = root / job["name"]
        manifest = read(directory / "manifest.json")
        if (
            manifest["status"] != "completed"
            or manifest["git_revision"] != status["revisions"][job["task"]]
        ):
            raise ValueError(f"Incomplete or changed source: {job['name']}")
        path = directory / "models/results.json"
        result = read(path)
        count = 6 if job["task"] == "zeva" else 3 if job["task"] == "flare" else 2
        seeds = result["seeds"]
        if len(result["results"]) != count * len(seeds):
            raise ValueError(f"Missing model results: {job['name']}")
        pairs = {(row["mode"], row["seed"]) for row in result["results"]}
        if len(pairs) != count * len(seeds) or {s for _, s in pairs} != set(seeds):
            raise ValueError(f"Repeated model result: {job['name']}")
        # Keep local provenance in the manifest; do not publish absolute checkpoints.
        for row in result["results"]:
            row.pop("checkpoint", None)
        if "data" in result:
            result["data"] = {
                k: v
                for k, v in result["data"].items()
                if k not in ("renderer", "gpu_uuid")
            }
        runs[job["name"]] = {
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "manifest": {
                k: manifest[k]
                for k in (
                    "git_revision",
                    "tracked_diff_sha256",
                    "seconds",
                    "device",
                    "torch",
                    "max_allocated_mib",
                    "max_reserved_mib",
                )
                if k in manifest
            },
            "results": result,
        }
    empirical = read(root / "zeva_2026/empirical/results.json")["results"]["test"][
        "mse"
    ]
    return {
        "as_of": "2026-09-30",
        "scope": "Completed development diagnostics, not robot success or transfer",
        "run": root.name,
        "fit_count": sum(len(v["results"]["results"]) for v in runs.values()),
        "started": status["started"],
        "finished": status["finished"],
        "zeva_empirical_test_mse": empirical,
        "runs": runs,
    }


def errorbar(ax, x, values, **kwargs):
    """Show initialization variability, not episode-level confidence bounds."""
    values = np.asarray(values)
    ax.errorbar(x, values.mean(0), yerr=values.std(0, ddof=1), capsize=3, **kwargs)


def collect_followup(path: Path, revision: str) -> dict:
    """Keep the adaptive follow-up separate from the predeclared matrix."""
    report = read(path / "results.json")
    modes = {"response_residual", "response_supported"}
    expected = {(mode, seed) for mode in modes for seed in report["seeds"]}
    pairs = {(row["mode"], row["seed"]) for row in report["results"]}
    if pairs != expected or len(pairs) != len(report["results"]) or not revision:
        raise ValueError("Incomplete follow-up or missing recorded launch revision")
    report["data"] = {
        k: v for k, v in report["data"].items() if k not in ("renderer", "gpu_uuid")
    }
    return {
        "scope": "Post-hoc development follow-up; not preregistered or sealed-test evidence",
        "recorded_launch_revision": revision,
        "source_sha256": hashlib.sha256(
            (path / "results.json").read_bytes()
        ).hexdigest(),
        "results": report,
    }


def figures(data: dict, directory: Path) -> None:
    """Render all comparison arms; no best-seed or best-test selection."""
    directory.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.3))
    a, b, c, d = axes.flat
    zeva = [
        row
        for name, entry in data["runs"].items()
        if name.startswith("zeva_")
        for row in entry["results"]["results"]
    ]
    modes = ("none", "recent", "archive", "full", "response", "response_residual")
    arrays = [
        [r["test"]["mse"] * 1e4 for r in zeva if r["mode"] == mode] for mode in modes
    ]
    a.bar(
        np.arange(7),
        [np.mean(v) for v in arrays] + [data["zeva_empirical_test_mse"] * 1e4],
        yerr=[np.std(v, ddof=1) for v in arrays] + [0],
        capsize=3,
        color=[COLORS["gray"]] * 4 + [COLORS["blue"], COLORS["teal"], COLORS["orange"]],
    )
    a.set(
        xticks=np.arange(7),
        xticklabels=[
            "None",
            "Recent",
            "Archive",
            "Full",
            "Response",
            "Prior +\nresidual",
            "Fixed\nprior",
        ],
        title="A  Retain useful interaction evidence",
        ylabel="Joint-change MSE x 10,000 (lower)",
    )
    a.tick_params(axis="x", labelsize=9)
    for anchor, style in ((0.0, "-"), (0.25, "--")):
        for mode, color in (("atomic", COLORS["teal"]), ("continuous", COLORS["blue"])):
            values = np.array(
                [
                    [
                        r["curve"][-1]["mean_reward"]
                        for r in data["runs"][f"jev_bc{bc}_anchor{anchor}"]["results"][
                            "results"
                        ]
                        if r["mode"] == mode
                    ]
                    for bc in (0.1, 7.0, 70.0)
                ]
            ).T
            errorbar(
                b,
                [0.1, 7, 70],
                values,
                label=f"{mode}; reference replacement {anchor:.0%}",
                marker="o",
                linestyle=style,
                color=color,
            )
    b.axhline(-1, linestyle=":", color=COLORS["gray"], label="Initial reference")
    b.set(
        xscale="log",
        title="B  Match regularization and data support",
        xlabel="BC weight",
        ylabel="Synthetic executed-action reward (higher)",
    )
    b.legend(fontsize=8)
    flare = [
        row
        for name, entry in data["runs"].items()
        if name.startswith("flare_") and name.endswith("_1000")
        for row in entry["results"]["results"]
    ]
    horizons = (1, 5, 10)
    for mode, label, color in (
        ("direct", "Direct", "blue"),
        ("residual", "Residual + actions", "teal"),
        ("action_free", "Residual, no actions", "orange"),
    ):
        values = [
            [r["horizons"][str(h)]["cosine_error"] for h in horizons]
            for r in flare
            if r["mode"] == mode
        ]
        errorbar(c, horizons, values, marker="o", label=label, color=COLORS[color])
    c.plot(
        horizons,
        [flare[0]["horizons"][str(h)]["persistence_cosine_error"] for h in horizons],
        "--",
        color=COLORS["gray"],
        label="Persistence",
    )
    for key, label, color in (
        ("cosine_error", "True commands", "teal"),
        ("shuffled_cosine_error", "Shuffled commands", "gray"),
        ("zero_arm_cosine_error", "Zero arm commands", "orange"),
        ("reversed_prefix_cosine_error", "Reversed valid prefix", "blue"),
    ):
        values = [
            [r["horizons"][str(h)][key] for h in horizons]
            for r in flare
            if r["mode"] == "residual"
        ]
        errorbar(d, horizons, values, marker="o", label=label, color=COLORS[color])
    for ax, title in (
        (c, "C  Frozen-feature prediction at 1000 updates"),
        (d, "D  Input sensitivity, not causal intervention"),
    ):
        ax.set(
            title=title,
            xlabel="Future control horizon",
            ylabel="Cosine error (lower)",
            xticks=horizons,
        )
        ax.legend(fontsize=8)
    for ax in axes.flat:
        ax.grid(axis="y", alpha=0.15)
    fig.suptitle(
        "Separate mechanism evidence from robot performance", fontsize=17, weight="bold"
    )
    fig.text(
        0.5,
        0.006,
        "A/C/D: six seeds; B: three seeds per arm. Error bars: sample SD across initializations, not confidence intervals. Reused development data.",
        ha="center",
        fontsize=8.2,
    )
    fig.tight_layout(rect=(0, 0.025, 1, 0.96), h_pad=2.2)
    export(fig, directory / "continuation-results")

    if "zeva_followup" in data:
        rows = data["zeva_followup"]["results"]["results"]
        empirical = data["zeva_empirical_test_mse"]
        empirical_late = data["zeva_empirical_late_mse"]
        fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.5))
        for ax, metric, prior, title in zip(
            axes,
            ("mse", "late_mse"),
            (empirical, empirical_late),
            ("All query times", "After at least four completed records"),
            strict=True,
        ):
            values = [
                [r["test"][metric] * 1e4 for r in rows if r["mode"] == mode]
                for mode in ("response_residual", "response_supported")
            ]
            ax.bar(
                [0, 1, 2],
                [prior * 1e4] + [np.mean(v) for v in values],
                yerr=[0] + [np.std(v, ddof=1) for v in values],
                capsize=4,
                color=[COLORS["gray"], COLORS["blue"], COLORS["teal"]],
            )
            ax.set(
                title=title,
                xticks=[0, 1, 2],
                xticklabels=[
                    "Fixed prior",
                    "Prior +\nresidual",
                    "Support-gated\nresidual",
                ],
                ylabel="Joint-change MSE x 10,000 (lower)",
            )
            ax.grid(axis="y", alpha=0.15)
        fig.suptitle(
            "Protect an informative empirical response", fontsize=16, weight="bold"
        )
        fig.text(
            0.5,
            0.005,
            "Post-hoc CPU diagnostic; six seeds, bars = sample SD. Same reused development split; no task-success or shift robustness claim.",
            ha="center",
            fontsize=7.8,
        )
        fig.tight_layout(rect=(0, 0.03, 1, 0.95))
        export(fig, directory / "zeva-support-followup")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_root", type=Path)
    parser.add_argument("--zeva-followup", type=Path)
    parser.add_argument("--followup-revision")
    args = parser.parse_args()
    data = collect(args.run_root)
    if args.zeva_followup:
        data["zeva_followup"] = collect_followup(
            args.zeva_followup, args.followup_revision
        )
        data["zeva_empirical_late_mse"] = read(
            args.run_root / "zeva_2026/empirical/results.json"
        )["results"]["test"]["late_mse"]
    target = ROOT / "data/continuation-2026-09-30.json"
    target.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    )
    figures(data, ROOT / "research/figures/continuation-2026-09-30")
    print(f"Published {data['fit_count']} fits: {target}")


if __name__ == "__main__":
    main()
