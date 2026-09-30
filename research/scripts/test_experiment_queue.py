"""Regression checks for the bounded diagnostic controller."""

import json

import pytest
from experiment_queue import experiment_plan, gpu_available, summarize


def test_plan_covers_three_branches_without_vla_or_gpu01():
    plan = experiment_plan()
    assert len(plan) == 11 and len({row["name"] for row in plan}) == 11
    assert {row["task"] for row in plan} == {"flare", "zeva", "jev"}
    assert all(row["steps"] <= 1000 for row in plan)
    assert all(
        ("--shared-gpu2" in row["extra"]) == (row["task"] == "flare") for row in plan
    )


@pytest.mark.parametrize(
    "free, expected", [("8191", False), ("9000", True), ("bad", False)]
)
def test_capacity_check_fails_closed(free, expected, monkeypatch, tmp_path):
    import builtins

    original = builtins.open
    monkeypatch.setattr("subprocess.check_output", lambda *a, **kw: free)
    monkeypatch.setattr(
        "builtins.open", lambda *a, **kw: original(tmp_path / "lease", "a")
    )
    assert gpu_available() == expected


def test_summary_keeps_negative_rewards_and_source(tmp_path):
    path = tmp_path / "jev_test/models"
    path.mkdir(parents=True)
    (path / "results.json").write_text(
        json.dumps(
            {
                "results": [
                    {"mode": "continuous", "seed": 1, "curve": [{"mean_reward": -9.0}]}
                ]
            }
        )
    )
    report = summarize(tmp_path)
    assert report[0]["mean_reward"] == -9.0
    assert report[0]["source"] == str(path / "results.json")
