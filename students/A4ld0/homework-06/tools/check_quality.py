"""Run from the homework folder: python tools/check_quality.py."""
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from time import perf_counter
from xml.etree import ElementTree

from report_assets import normalize_report_assets

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)
environment = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTHONUTF8="1")


def pytest_run(arguments, log_name):
    started = perf_counter()
    result = subprocess.run([sys.executable, "-m", "pytest", *arguments], cwd=ROOT,
                            env=environment, text=True, encoding="utf-8",
                            capture_output=True, check=False)
    elapsed = perf_counter() - started
    output = result.stdout + result.stderr
    (EVIDENCE / log_name).write_text(output, encoding="utf-8")
    print(output, end="")
    if result.returncode:
        raise SystemExit(result.returncode)
    return elapsed


duration = pytest_run(["-q", "--junitxml=docs/evidence/test-results.xml"], "tests.txt")
suite = ElementTree.parse(EVIDENCE / "test-results.xml").getroot().find("testsuite")
suite_duration = float(suite.attrib["time"])
complete = all(int(suite.attrib[key]) == 0 for key in ("failures", "errors", "skipped"))
pytest_run(["-p", "pytest_cov", "-q", "--cov=src", "--cov-branch",
            "--cov-report=term-missing", "--cov-report=html:coverage",
            "--cov-report=json:docs/evidence/coverage.json"], "coverage.txt")
normalize_report_assets(ROOT)
totals = json.loads((EVIDENCE / "coverage.json").read_text(encoding="utf-8"))["totals"]
statements = 100 * totals["covered_lines"] / totals["num_statements"]
branches = 100 * totals["covered_branches"] / totals["num_branches"]
quality = {"python": platform.python_version(), "statement_percent": statements,
           "branch_percent": branches, "suite_process_seconds": round(duration, 4),
           "suite_seconds": suite_duration, "no_failures_or_skips": complete,
           "statement_requirement_met": statements > 90,
           "branch_requirement_met": branches > 85, "speed_requirement_met": suite_duration < 2}
(EVIDENCE / "quality.json").write_text(json.dumps(quality, indent=2) + "\n", encoding="utf-8")
print(json.dumps(quality, indent=2))
if not all(quality[key] for key in ("statement_requirement_met", "branch_requirement_met",
                                   "speed_requirement_met", "no_failures_or_skips")):
    raise SystemExit("Quality thresholds were not met; see docs/evidence/quality.json")
