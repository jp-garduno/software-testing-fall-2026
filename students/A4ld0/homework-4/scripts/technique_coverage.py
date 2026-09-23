"""Measure each technique alone for the analysis, preserving full-suite evidence."""

import json
import os
from pathlib import Path
import sys

from command_runner import capture_command

ROOT = Path(__file__).resolve().parents[1]
TECHNIQUES = {
    "EP": ("test_equivalence_partitioning.py", "equivalencePartitioning.test.js"),
    "BV": ("test_boundary_values.py", "boundaryValues.test.js"),
    "DT": ("test_decision_tables.py", "decisionTables.test.js"),
    "ST": ("test_state_transitions.py", "stateTransitions.test.js"),
}


def main():
    """Record isolated coverage measurements without replacing full-run evidence."""
    (ROOT / "tmp").mkdir(exist_ok=True)
    results = {}
    env = dict(os.environ, FORCE_COLOR="0", NO_COLOR="1")
    for technique, (python_file, js_file) in TECHNIQUES.items():
        target = f"tmp/{technique}-python.json"
        python_env = dict(
            env, COVERAGE_FILE=str(ROOT / "tmp" / f".coverage-{technique}")
        )
        commands = [
            (
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    f"tests/{python_file}",
                    "-q",
                    "--cov=src.banking_system",
                    "--cov-branch",
                    f"--cov-report=json:{target}",
                ],
                python_env,
            ),
            (
                [
                    "node",
                    "node_modules/jest/bin/jest.js",
                    "--runInBand",
                    "--runTestsByPath",
                    f"tests/{js_file}",
                    "--coverage",
                    "--coverageThreshold={}",
                    f"--coverageDirectory=tmp/{technique}-js",
                ],
                env,
            ),
        ]
        for command, command_env in commands:
            result = capture_command(command, ROOT, command_env)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
        py = json.loads((ROOT / target).read_text(encoding="utf-8"))["totals"]
        js = json.loads(
            (ROOT / f"tmp/{technique}-js/coverage-summary.json").read_text(
                encoding="utf-8"
            )
        )["total"]
        results[technique] = {
            "python_lines": round(100 * py["covered_lines"] / py["num_statements"], 2),
            "python_branches": round(
                100 * py["covered_branches"] / py["num_branches"], 2
            ),
            "javascript_lines": js["lines"]["pct"],
            "javascript_branches": js["branches"]["pct"],
        }
    (ROOT / "reports/technique-coverage.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
