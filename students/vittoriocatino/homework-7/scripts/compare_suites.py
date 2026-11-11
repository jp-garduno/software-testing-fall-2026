"""Measure equivalent suites and save reproducible LOC/runtime evidence."""

import ast
import csv
import json
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def source_metrics(path):
    """Count physical and nonblank/noncomment lines, including docstrings."""
    text = path.read_text(encoding="utf-8")
    return {
        "physical_lines": len(text.splitlines()),
        "nonblank_noncomment_lines": sum(
            bool(line.strip()) and not line.lstrip().startswith("#")
            for line in text.splitlines()
        ),
    }


def main():
    """Run each ten-case suite five times in fresh pytest subprocesses."""
    traditional = ROOT / "tests/test_order_traditional.py"
    with (ROOT / "test_data/order_calculations.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        scenarios = [row["test_name"] for row in list(csv.DictReader(stream))[:10]]
    names = [
        node.name.removeprefix("test_")
        for node in ast.parse(traditional.read_text(encoding="utf-8")).body
        if isinstance(node, ast.FunctionDef)
    ]
    if names != scenarios:
        raise ValueError("The comparison suites must cover the same ten scenarios")
    results = {
        "python": sys.version.split()[0],
        "scenarios": scenarios,
        "repetitions": 5,
        "suites": {},
    }
    for name in ("traditional", "data_driven"):
        path = ROOT / f"tests/test_order_{name}.py"
        durations = []
        for _ in range(5):
            start = time.perf_counter()
            subprocess.run(
                [sys.executable, "-m", "pytest", "-q", str(path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            durations.append(time.perf_counter() - start)
        results["suites"][name] = {
            **source_metrics(path),
            "wall_seconds": durations,
            "median_seconds": statistics.median(durations),
        }
    original = results["suites"]["traditional"]["nonblank_noncomment_lines"]
    parameterized = results["suites"]["data_driven"]["nonblank_noncomment_lines"]
    results["test_code_reduction_percent"] = round(
        (original - parameterized) / original * 100, 2
    )
    output = ROOT / "reports/comparison_metrics.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
