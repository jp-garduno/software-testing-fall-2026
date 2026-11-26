import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from todo_backends import BACKENDS, HOMEWORK_ROOT, load_todo_backend


PYTEST_CASES = 11
BEHAVE_SCENARIOS = 6


def run_command(command, env):
    return subprocess.run(
        command,
        cwd=HOMEWORK_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def run_backend(backend):
    backend_module = load_todo_backend(backend)
    setup_started = time.perf_counter()
    page = backend_module.create_todo_page()
    try:
        page.navigate()
        setup_seconds = time.perf_counter() - setup_started
    finally:
        page.close()

    suite_started = time.perf_counter()
    env = os.environ.copy()
    env["TODO_BACKEND"] = backend
    env["COVERAGE_FILE"] = str(HOMEWORK_ROOT / f".coverage.{backend}")
    source_file = HOMEWORK_ROOT / backend / "pages" / "todo_page.py"
    include_option = f"--include={source_file.resolve()}"

    commands = (
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            include_option,
            "-m",
            "pytest",
            "-q",
        ],
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "--append",
            include_option,
            "-m",
            "behave",
            "--no-capture",
            "-f",
            "plain",
        ],
    )
    outputs = []
    return_code = 0
    for command in commands:
        result = run_command(command, env)
        outputs.append(result.stdout + result.stderr)
        if result.returncode:
            return_code = result.returncode

    coverage_result = run_command(
        [
            sys.executable,
            "-m",
            "coverage",
            "report",
            f"--include={source_file.resolve()}",
        ],
        env,
    )
    outputs.append(coverage_result.stdout + coverage_result.stderr)
    if coverage_result.returncode:
        return_code = coverage_result.returncode

    elapsed = time.perf_counter() - suite_started
    average = elapsed / (PYTEST_CASES + BEHAVE_SCENARIOS)
    return backend, setup_seconds, elapsed, average, return_code, outputs


def main():
    with ThreadPoolExecutor(max_workers=len(BACKENDS)) as executor:
        results = list(executor.map(run_backend, BACKENDS))

    result_code = 0
    for backend, setup, elapsed, average, return_code, outputs in results:
        print(f"\n=== {backend.title()} ===")
        print(f"Setup (browser launch + navigation): {setup:.2f}s")
        print(f"Test suite total: {elapsed:.2f}s")
        print(f"Average per test ({PYTEST_CASES + BEHAVE_SCENARIOS} tests): {average:.2f}s")
        for output in outputs:
            print(output, end="")
        if return_code:
            result_code = return_code

    return result_code


if __name__ == "__main__":
    raise SystemExit(main())
