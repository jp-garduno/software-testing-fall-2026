"""Run from the homework folder: python tools/check_quality.py."""
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)
environment = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTHONUTF8="1")


def pytest_run(arguments, log_name):
    started = perf_counter()
    result = subprocess.run([sys.executable, "-m", "pytest", *arguments], cwd=ROOT,
                            env=environment, text=True, encoding="utf-8",
                            capture_output=True)
    elapsed = perf_counter() - started
    output = result.stdout + result.stderr
    (EVIDENCE / log_name).write_text(output, encoding="utf-8")
    print(output, end="")
    if result.returncode:
        raise SystemExit(result.returncode)
    return elapsed


duration = pytest_run(["-q"], "tests.txt")
pytest_run(["-p", "pytest_cov", "-q", "--cov=src", "--cov-branch",
            "--cov-report=term-missing", "--cov-report=html:coverage",
            "--cov-report=json:docs/evidence/coverage.json"], "coverage.txt")
totals = json.loads((EVIDENCE / "coverage.json").read_text(encoding="utf-8"))["totals"]
statements = 100 * totals["covered_lines"] / totals["num_statements"]
branches = 100 * totals["covered_branches"] / totals["num_branches"]
