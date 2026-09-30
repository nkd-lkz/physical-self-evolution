"""Run a predeclared diagnostic matrix with a twelve-hour wall-clock ceiling.

Only cached small models may share GPU 2. The separate exclusive online queue
keeps its idle requirement. This controller never touches other process groups.
"""

import argparse
import fcntl
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = Path("/home/luokz/rlinf_rlt")


def experiment_plan() -> list[dict]:
    """Declare all arms before looking at their results; no test-set promotion."""
    jobs = []
    for seed in (2026, 2029):
        jobs.append(
            {
                "name": f"zeva_{seed}",
                "task": "zeva",
                "seed": seed,
                "steps": 1000,
                "extra": [],
            }
        )
    for bc in (0.1, 7.0, 70.0):
        for anchor in (0.0, 0.25):
            jobs.append(
                {
                    "name": f"jev_bc{bc}_anchor{anchor}",
                    "task": "jev",
                    "seed": 2029,
                    "steps": 1000,
                    "extra": [
                        "--jev-data-mode",
                        "mixed",
                        "--actor-start",
                        "300",
                        "--actor-lr",
                        "0.0001",
                        "--bc-weight",
                        str(bc),
                        "--reference-fraction",
                        str(anchor),
                    ],
                }
            )
    for seed, steps in ((2026, 250), (2026, 1000), (2029, 1000)):
        jobs.append(
            {
                "name": f"flare_{seed}_{steps}",
                "task": "flare",
                "seed": seed,
                "steps": steps,
                "extra": ["--shared-gpu2"],
            }
        )
    return jobs


def gpu_available() -> bool:
    """Inspect capacity and the project lease without creating a CUDA context."""
    try:
        free = int(
            subprocess.check_output(
                [
                    "nvidia-smi",
                    "-i",
                    "2",
                    "--query-gpu=memory.free",
                    "--format=csv,noheader,nounits",
                ],
                text=True,
                timeout=15,
            ).strip()
        )
        if free < 8192:
            return False
        with open("/tmp/rlt-atomic-gpu2.lock", "a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except (OSError, ValueError, subprocess.SubprocessError):
        return False


def revision(root: Path) -> str:
    """Require a clean checkout before recording a reproducible revision."""
    if subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=root, text=True
    ).strip():
        raise RuntimeError(f"Dirty checkout: {root}")
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True
    ).strip()


def save_status(output: Path, status: dict) -> None:
    """Publish a complete status snapshot without exposing a partial JSON file."""
    temporary = output / "status.tmp"
    temporary.write_text(json.dumps(status, indent=2, allow_nan=False) + "\n")
    temporary.replace(output / "status.json")


def summarize(output: Path) -> list[dict]:
    """Collect completed models, retaining negative outcomes and provenance paths."""
    rows = []
    for report_path in sorted(output.glob("*/models/results.json")):
        report = json.loads(report_path.read_text())
        for row in report["results"]:
            summary = {
                "experiment": report_path.parent.parent.name,
                "source": str(report_path),
                "mode": row["mode"],
                "seed": row["seed"],
            }
            if "curve" in row:
                summary.update(row["curve"][-1])
            elif "test" in row:
                summary.update(mse=row["test"]["mse"], best_step=row["best_step"])
            else:
                summary["horizons"] = row["horizons"]
            rows.append(summary)
    (output / "summary.json").write_text(
        json.dumps(rows, indent=2, allow_nan=False) + "\n"
    )
    return rows


def stop_owned(process: subprocess.Popen) -> None:
    """Terminate only the child process group created by this controller."""
    if process.poll() is None:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--hours", type=float, default=12)
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if not 0 < args.hours <= 12:
        parser.error("Use a positive budget of at most 12 hours")
    plan = experiment_plan()
    if not args.run:
        print(json.dumps(plan, indent=2))
        return
    args.output.mkdir(parents=True, exist_ok=False)
    revisions = {
        task: revision(CODE / f"UPT_{task}_dev") for task in ("flare", "zeva", "jev")
    }
    status = {
        "status": "running",
        "started": time.time(),
        "revisions": revisions,
        "plan": plan,
        "completed": [],
        "budget_hours": args.hours,
        "scope": "Diagnostics, not robot success",
    }
    deadline = time.monotonic() + args.hours * 3600
    env = {
        **os.environ,
        "CUDA_VISIBLE_DEVICES": "",
        "OMP_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
    }

    def interrupt(signum, frame):
        raise KeyboardInterrupt(f"Signal {signum}")

    signal.signal(signal.SIGTERM, interrupt)
    try:
        with open(f"/tmp/rlt-diagnostic-queue-{os.getuid()}.lock", "a") as lease:
            fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
            for job in plan:
                status.update(
                    current=job["name"],
                    heartbeat=time.time(),
                    status="waiting_resources",
                )
                save_status(args.output, status)
                while "--shared-gpu2" in job["extra"] and not gpu_available():
                    if time.monotonic() >= deadline:
                        raise TimeoutError("Resource wait exhausted wall-clock budget")
                    status["heartbeat"] = time.time()
                    save_status(args.output, status)
                    time.sleep(min(30, max(0, deadline - time.monotonic())))
                if deadline <= time.monotonic():
                    raise TimeoutError("Experiment budget exhausted")
                if revision(CODE / f"UPT_{job['task']}_dev") != revisions[job["task"]]:
                    raise RuntimeError("Checkout changed while queued")
                command = [
                    sys.executable,
                    "-u",
                    str(HERE / "shared_gpu_audit.py"),
                    job["task"],
                    "--output",
                    str(args.output / job["name"]),
                    "--steps",
                    str(job["steps"]),
                    "--seed-start",
                    str(job["seed"]),
                    *job["extra"],
                ]
                with (args.output / f"{job['name']}.log").open("x") as log:
                    process = subprocess.Popen(
                        command,
                        env=env,
                        stdout=log,
                        stderr=subprocess.STDOUT,
                        start_new_session=True,
                        cwd=HERE,
                    )
                    status.update(status="running", child_pid=process.pid)
                    save_status(args.output, status)
                    try:
                        job_deadline = min(deadline, time.monotonic() + 3600)
                        while process.poll() is None:
                            if time.monotonic() >= job_deadline:
                                raise TimeoutError("Child exceeded its bounded runtime")
                            try:
                                process.wait(
                                    timeout=min(
                                        30, max(0.1, job_deadline - time.monotonic())
                                    )
                                )
                            except subprocess.TimeoutExpired:
                                status["heartbeat"] = time.time()
                                save_status(args.output, status)
                        if process.returncode:
                            raise RuntimeError(
                                f"{job['name']} exited {process.returncode}; later jobs stopped"
                            )
                    finally:
                        stop_owned(process)
                status["completed"].append(job["name"])
                summarize(args.output)
                save_status(args.output, status)
            status.update(status="completed", current=None, child_pid=None)
    except BaseException as exc:
        status.update(status="stopped", error=f"{type(exc).__name__}: {exc}")
        raise
    finally:
        status["finished"] = time.time()
        summarize(args.output)
        save_status(args.output, status)


if __name__ == "__main__":
    main()
