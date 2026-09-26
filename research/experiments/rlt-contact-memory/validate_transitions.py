#!/usr/bin/env python3
"""Validate declared transition contracts, not sensor truth or learning quality."""
import argparse
import json
import math
from pathlib import Path
import sys

INPUTS = {"images", "proprioception", "task", "past_executed_commands",
          "past_durations", "frozen_features"}
CONTROLLERS = {"base", "actor", "expert"}
SPLITS = {"train", "dev", "test"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def finite_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def vector(x):
    return isinstance(x, list) and bool(x) and all(finite_number(v) for v in x)


def validate(row):
    for key in ("episode_id", "instance_id", "condition_id", "action_space", "feature_version"):
        require(isinstance(row.get(key), str) and bool(row[key].strip()), f"missing {key}")
    require(row.get("split") in SPLITS, "unknown split")
    require(row.get("controller") in CONTROLLERS, "unknown controller")
    require(row.get("feature_tap") in {"prefix", "action_head"}, "unknown feature_tap")
    fields = row.get("deploy_fields")
    require(isinstance(fields, list) and bool(fields) and
            all(isinstance(x, str) and x in INPUTS for x in fields),
            "deploy_fields includes unknown, teacher-only or future inputs")
    for key in ("decision_time_s", "history_latest_time_s", "dt_s", "elapsed_s"):
        require(finite_number(row.get(key)), f"non-finite or absent {key}")
    require(0 <= row["history_latest_time_s"] <= row["decision_time_s"], "history leaks future time")
    for key in ("H", "C_requested", "C_executed"):
        require(type(row.get(key)) is int and row[key] > 0, f"invalid {key}")
    require(row["C_executed"] <= row["C_requested"] <= row["H"], "invalid chunk lengths")
    require(row["dt_s"] > 0 and row["elapsed_s"] > 0, "nonpositive duration")
    require(math.isclose(row["elapsed_s"], row["C_executed"] * row["dt_s"],
                         rel_tol=1e-6, abs_tol=1e-8), "elapsed time does not match executed prefix")
    commands = row.get("u_exec")
    require(isinstance(commands, list) and len(commands) == row["C_executed"],
            "u_exec length does not match C_executed")
    require(all(vector(a) for a in commands), "invalid command values")
    require(len({len(a) for a in commands}) == 1, "inconsistent command dimensions")
    labels, masks = row.get("measured"), row.get("valid")
    require(isinstance(labels, dict) and isinstance(masks, dict), "missing measured/valid")
    for key in ("delta_q", "delta_ee", "contact_event"):
        require(key in labels and type(masks.get(key)) is bool, f"missing label or mask: {key}")
        if not masks[key]:
            require(labels[key] is None, f"missing {key} must be null, not a negative label")
        elif key == "contact_event":
            require(type(labels[key]) is int and labels[key] in (0, 1), "invalid contact event")
        else:
            require(vector(labels[key]), f"invalid {key}")
            if key == "delta_ee":
                require(len(labels[key]) == 3, "delta_ee must be a 3D translation")
    require(any(masks[k] for k in ("delta_q", "delta_ee", "contact_event")), "no valid targets")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path)
    args = parser.parse_args()
    instances, episodes, samples = {}, {}, set()
    count = 0
    try:
        with args.jsonl.open(encoding="utf-8") as f:
            for line_number, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    require(isinstance(row, dict), "row must be an object")
                    validate(row)
                    for index, key in ((instances, "instance_id"), (episodes, "episode_id")):
                        require(index.setdefault(row[key], row["split"]) == row["split"],
                                f"{key} crosses data splits")
                    identity = row["episode_id"], row["decision_time_s"]
                    require(identity not in samples, "duplicate transition")
                    samples.add(identity)
                    count += 1
                except (ValueError, TypeError, KeyError) as exc:
                    raise ValueError(f"line {line_number}: {exc}") from exc
        require(count > 0, "empty dataset")
    except (ValueError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: {count} records; declared fields, timing and instance splits checked. "
          "Sensor truth, feature leakage and model performance are NOT verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
