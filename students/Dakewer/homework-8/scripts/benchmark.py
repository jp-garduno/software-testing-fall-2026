#!/usr/bin/env python3
"""Run both end-to-end suites several times and summarise the timings.

Run from an activated virtualenv after `npm install` in playwright/:

    TODO_URL=http://127.0.0.1:7002/ python scripts/benchmark.py --runs 5
"""
import argparse
import json
import os
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
PLAYWRIGHT = ROOT / "playwright" / "node_modules" / "@playwright" / "test" / "cli.js"


def selenium(scope):
    command = [sys.executable, "-m", "pytest", "-q", "-p", "pytest_timing", "-p", "no:cacheprovider"]
    env = {"SELENIUM_DRIVER_SCOPE": scope, "PYTHONPATH": str(SCRIPTS)}
    return command, ROOT / "selenium", env


def playwright(workers, channel=""):
    command = [
        "node", str(PLAYWRIGHT), "test", "--project=chromium", f"--workers={workers}",
        "--retries=0", "--trace=off",
        f"--reporter={SCRIPTS / 'playwright-timing-reporter.js'}",
    ]
    return command, ROOT / "playwright", {"PW_CHANNEL": channel}


CONFIGURATIONS = {
    "Selenium, new browser per test": selenium("function"),
    "Selenium, shared browser": selenium("session"),
    "Playwright, 1 worker, full Chromium": playwright(1, "chromium"),
    "Playwright, 1 worker, headless shell": playwright(1),
    "Playwright, 2 workers, headless shell": playwright(2),
}


def run_once(command, cwd, extra_env):
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "timing.json"
        env = {**os.environ, **extra_env, "BENCH_OUT": str(out)}
        start = time.perf_counter()
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, check=False)
        wall = time.perf_counter() - start
        if result.returncode != 0:
            sys.exit(f"Suite failed:\n{result.stdout}\n{result.stderr}")
        data = json.loads(out.read_text())
    if "total" not in data:  # pytest reports one figure per phase
        data["total"] = data["setup"] + data["call"] + data["teardown"]
    return {
        "tests": data["tests"],
        "wall_s": wall,
        "per_test_s": data["total"] / data["tests"],
        "setup_per_test_s": data["setup"] / data["tests"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args()

    results = {name: [] for name in CONFIGURATIONS}
    # Interleave configurations so that machine drift affects all of them equally.
    for number in range(1, args.runs + 1):
        for name, configuration in CONFIGURATIONS.items():
            results[name].append(run_once(*configuration))
            print(f"run {number}: {name}: {results[name][-1]['wall_s']:.2f}s", flush=True)

    lines = [
        "| Configuration | Tests | Total wall time (s) | Min-max (s) | Avg per test (s) | Setup per test (s) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, runs in results.items():
        walls = [r["wall_s"] for r in runs]
        lines.append(
            f"| {name} | {runs[0]['tests']} | {statistics.median(walls):.2f} "
            f"| {min(walls):.2f}-{max(walls):.2f} "
            f"| {statistics.median(r['per_test_s'] for r in runs):.3f} "
            f"| {statistics.median(r['setup_per_test_s'] for r in runs):.3f} |"
        )
    table = "\n".join(lines)

    output = ROOT / "reports" / "benchmark"
    output.mkdir(parents=True, exist_ok=True)
    (output / "benchmark.json").write_text(json.dumps(results, indent=2))
    (output / "benchmark.md").write_text(table + "\n")
    print(f"\nMedians of {args.runs} runs\n\n{table}")


if __name__ == "__main__":
    main()
