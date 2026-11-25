"""Run the equivalent Selenium and Playwright suites several times and record timings and code size.

Both suites run the same 20 tests, one at a time, on Chromium. Writes reports/benchmark.json.
Run from anywhere: python scripts/benchmark.py
"""

import json
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAYWRIGHT_DIR = ROOT / "playwright"
RUNS = 5

SUITES = {
    "selenium": (ROOT, [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-q", "selenium/tests"]),
    "playwright": (PLAYWRIGHT_DIR, ["npx", "playwright", "test", "--project=chromium", "--workers=1", "--reporter=line"]),
    "playwright_parallel": (PLAYWRIGHT_DIR, ["npx", "playwright", "test", "--project=chromium", "--reporter=line"]),
}

CODE_FILES = {
    "Page object": {
        "selenium": ["selenium/pages/todo_page.py"],
        "playwright": ["playwright/pages/TodoPage.js"],
    },
    "Tests": {
        "selenium": ["selenium/tests/test_todo_crud.py", "selenium/tests/test_todo_filter.py"],
        "playwright": ["playwright/tests/todo-crud.spec.js", "playwright/tests/todo-filter.spec.js"],
    },
    "Setup and configuration": {
        "selenium": ["selenium/driver_factory.py", "selenium/tests/conftest.py", "pytest.ini"],
        "playwright": ["playwright/playwright.config.js", "playwright/tests/fixtures.js"],
    },
}

COMMENT_PREFIXES = ("#", "//", "/*", "*", '"""')


def count_code_lines(path):
    """Lines that are neither blank nor a comment or one-line docstring."""
    lines = (line.strip() for line in path.read_text(encoding="utf-8").splitlines())
    return sum(1 for line in lines if line and not line.startswith(COMMENT_PREFIXES))


def run_suite(cwd, command):
    start = time.perf_counter()
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    elapsed = time.perf_counter() - start
    if result.returncode != 0:
        raise RuntimeError(f"Suite failed, timings would be meaningless:\n{result.stdout}\n{result.stderr}")
    return elapsed


def measure_setup(cwd, command):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout.strip().splitlines()[-1])


def main():
    report = {"runs": RUNS, "tests_per_suite": 20, "timings": {}}
    samples = {name: [] for name in SUITES}
    # Alternate the suites so a slow network moment does not penalise only one of them.
    for _ in range(RUNS):
        for name, (cwd, command) in SUITES.items():
            samples[name].append(run_suite(cwd, command))
    for name, values in samples.items():
        report["timings"][name] = {"median": statistics.median(values), "min": min(values), "max": max(values)}

    report["setup"] = {
        "selenium": measure_setup(ROOT, [sys.executable, "scripts/measure_setup.py"]),
        "playwright": measure_setup(PLAYWRIGHT_DIR, ["node", "scripts/measure-setup.js"]),
    }
    report["lines_of_code"] = {
        area: {tool: sum(count_code_lines(ROOT / name) for name in files) for tool, files in tools.items()}
        for area, tools in CODE_FILES.items()
    }

    output = ROOT / "reports" / "benchmark.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    sys.stdout.write(output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
