"""Execute both browser suites and BDD, retaining honest output and timings."""

import json
import subprocess
import sys
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]


def run(name, arguments):
    """Save actual process output and fail the workflow when any suite fails."""
    started = perf_counter()
    process = subprocess.run(
        [sys.executable, "-m", *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    (ROOT / "reports" / f"{name}-results.txt").write_text(
        process.stdout + process.stderr, encoding="utf-8"
    )
    print(process.stdout, end="")
    if process.returncode:
        print(process.stderr, file=sys.stderr)
        raise SystemExit(process.returncode)
    return {
        "suite": name,
        "wall_seconds": perf_counter() - started,
        "exit_code": process.returncode,
    }


def main():
    """Run framework processes sequentially so their metrics do not overlap."""
    (ROOT / "reports").mkdir(exist_ok=True)
    results = []
    for engine in ("selenium", "playwright"):
        results.append(
            run(
                engine,
                [
                    "pytest",
                    f"{engine}/tests",
                    "-q",
                    f"--junitxml=reports/{engine}-junit.xml",
                ],
            )
        )
    results.append(
        run(
            "bdd",
            [
                "behave",
                "features",
                "--junit",
                "--junit-directory",
                "reports/bdd-junit",
                "-f",
                "json.pretty",
                "-o",
                "reports/bdd.json",
                "-f",
                "progress",
                "-o",
                "reports/bdd-progress.txt",
            ],
        )
    )
    (ROOT / "reports/execution-summary.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
