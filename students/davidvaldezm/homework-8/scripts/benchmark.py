"""Run equivalent suites sequentially and preserve auditable wall-clock data."""

import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "reports/live"


def run(command, cwd, name):
    """Record the full log and fail on a nonzero test exit code."""
    start = perf_counter()
    result = subprocess.run(
        command, cwd=cwd, text=True, capture_output=True, check=False
    )
    (LIVE / f"{name}.txt").write_text(result.stdout + result.stderr, encoding="utf-8")
    print(result.stdout)
    result.check_returncode()
    return perf_counter() - start


def main():
    """Measure warmed dependencies, one worker, identical headless Chrome."""
    LIVE.mkdir(parents=True, exist_ok=True)
    selenium_wall = run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-v",
            "--cov=selenium/pages",
            "--cov-report=term-missing",
            "--cov-report=json:reports/live/coverage.json",
            "--junitxml=reports/live/selenium-results.xml",
        ],
        ROOT,
        "selenium",
    )
    xml = ElementTree.parse(LIVE / "selenium-results.xml")
    cases = xml.findall(".//testcase")
    selenium_setup = [
        float(case.find("properties/property[@name='setup_seconds']").attrib["value"])
        for case in cases
    ]
    npm = shutil.which("npm.cmd" if os.name == "nt" else "npm")
    playwright_wall = run(
        [npm, "test", "--", "--workers=1"], ROOT / "playwright", "playwright"
    )
    pw = json.loads((LIVE / "playwright-results.json").read_text(encoding="utf-8"))
    setup_ms = []

    def collect(suite):
        for spec in suite.get("specs", []):
            for test in spec["tests"]:
                setup_ms.extend(
                    float(annotation["description"])
                    for annotation in test["annotations"]
                    if annotation["type"] == "setup_ms"
                )
        for child in suite.get("suites", []):
            collect(child)

    for suite in pw["suites"]:
        collect(suite)
    metrics = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "node": subprocess.check_output(["node", "--version"], text=True).strip(),
        "url": os.getenv("TODO_URL", "https://todomvc.com/examples/react/dist/"),
        "workers": 1,
        "retries": 0,
        "selenium": {
            "tests": len(cases),
            "wall_seconds": selenium_wall,
            "average_seconds": selenium_wall / len(cases),
            "mean_setup_seconds": sum(selenium_setup) / len(selenium_setup),
        },
        "playwright": {
            "tests": pw["stats"]["expected"],
            "wall_seconds": playwright_wall,
            "average_seconds": playwright_wall / pw["stats"]["expected"],
            "mean_setup_seconds": sum(setup_ms) / len(setup_ms) / 1000,
        },
    }
    (LIVE / "benchmark.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
