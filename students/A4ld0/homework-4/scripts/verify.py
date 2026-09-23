"""Run equivalent suites, preserve real output, and verify bonus thresholds.

Run with the Python environment containing requirements.txt. Node must be on PATH.
"""

import json
import os
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

from command_runner import capture_command

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)
ENV = dict(os.environ, FORCE_COLOR="0", NO_COLOR="1")


def run(command, output):
    """Save both output streams and abort verification on a failing command."""
    result = capture_command(command, ROOT, ENV)
    # Jest writes its verbose results to stderr, so preserve both streams.
    text = result.stdout + result.stderr
    (REPORTS / output).write_text(text, encoding="utf-8")
    print(text[-3500:])
    if result.returncode:
        raise SystemExit(f"Verification failed: {output} (exit {result.returncode})")


def main():
    """Run both suites and enforce matching case IDs and coverage thresholds."""
    # Windows terminals may default to cp1252; Jest emits Unicode check marks.
    sys.stdout.reconfigure(encoding="utf-8")
    run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-v",
            "--color=no",
            "--cov=src.banking_system",
            "--cov-branch",
            "--cov-fail-under=81",
            "--cov-report=term-missing",
            "--cov-report=html",
            "--cov-report=json:reports/python-coverage.json",
            "--junitxml=reports/python-results.xml",
        ],
        "python-results.txt",
    )
    run(
        [
            "node",
            "node_modules/jest/bin/jest.js",
            "--runInBand",
            "--coverage",
            "--verbose",
            "--json",
            "--outputFile=reports/javascript-results.json",
        ],
        "javascript-results.txt",
    )
    cases = json.loads((ROOT / "design/cases.json").read_text(encoding="utf-8"))
    expected = {case["id"] for case in cases}
    assert len(expected) == len(cases), "Duplicate design IDs"
    python_tests = ET.parse(REPORTS / "python-results.xml").findall(".//testcase")
    javascript = json.loads(
        (REPORTS / "javascript-results.json").read_text(encoding="utf-8")
    )
    js_tests = [
        test
        for suite in javascript["testResults"]
        for test in suite["assertionResults"]
    ]
    for language, tests, name_key in [
        ("Python", python_tests, "name"),
        ("JavaScript", js_tests, "title"),
    ]:
        names = [test.get(name_key) for test in tests]
        ids = [re.search(r"(?:EP|BV|DT|ST)[0-9]+", name).group() for name in names]
        assert (
            len(ids) == len(expected) and set(ids) == expected
        ), f"{language} case mismatch"
    python_coverage = json.loads(
        (REPORTS / "python-coverage.json").read_text(encoding="utf-8")
    )["totals"]
    js_coverage = json.loads(
        (ROOT / "coverage/coverage-summary.json").read_text(encoding="utf-8")
    )["total"]
    line_pct = (
        100 * python_coverage["covered_lines"] / python_coverage["num_statements"]
    )
    branch_pct = (
        100 * python_coverage["covered_branches"] / python_coverage["num_branches"]
    )
    assert (
        min(
            line_pct,
            branch_pct,
            js_coverage["lines"]["pct"],
            js_coverage["branches"]["pct"],
        )
        > 80
    )
    (REPORTS / "javascript-coverage-summary.json").write_text(
        json.dumps(js_coverage, indent=2) + "\n", encoding="utf-8"
    )
    summary = {
        "cases_per_language": len(cases),
        "case_ids_match": True,
        "python": {"line_percent": line_pct, "branch_percent": branch_pct},
        "javascript": {key: value["pct"] for key, value in js_coverage.items()},
    }
    (REPORTS / "verification-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
