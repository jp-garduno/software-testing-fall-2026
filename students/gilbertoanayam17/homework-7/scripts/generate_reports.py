"""Regenerate the two result files of the submission.

  test_results.txt      output of the whole suite (pytest -v) with the coverage table
  coverage_report.html  the same coverage data as one self-contained HTML page

The page is a single file with no JavaScript, built from the JSON report of
coverage.py, instead of the multi-file site that `coverage html` produces.

Run from the homework-7 directory:  python scripts/generate_reports.py
"""

import html
import json
import subprocess
import sys
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent

PAGE = Template(
    """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Coverage report - Homework 7</title>
    <style>
      body { font-family: system-ui, "Segoe UI", sans-serif; color: #0b0b0b; margin: 2.5rem; }
      h1 { font-size: 1.4rem; margin-bottom: 0.25rem; }
      .total { font-size: 2.5rem; font-weight: 600; margin: 0; }
      .muted { color: #52514e; }
      table { border-collapse: collapse; margin-top: 1.5rem; }
      th, td { padding: 0.45rem 1rem; text-align: right; border-bottom: 1px solid #e1e0d9; }
      th { color: #52514e; font-weight: 600; }
      th:first-child, td:first-child { text-align: left; }
      tfoot td { font-weight: 600; border-bottom: none; }
    </style>
  </head>
  <body>
    <h1>Coverage report - Homework 7: Data-Driven Test Suite</h1>
    <p class="total">$total_percent</p>
    <p class="muted">of the statements in <code>src/</code> were executed by the test suite ($tests).</p>
    <table>
      <thead>
        <tr><th>File</th><th>Statements</th><th>Missed</th><th>Coverage</th><th>Missing lines</th></tr>
      </thead>
      <tbody>
$rows
      </tbody>
      <tfoot>
        <tr><td>Total</td><td>$statements</td><td>$missed</td><td>$total_percent</td><td></td></tr>
      </tfoot>
    </table>
    <p class="muted">
      Measured with coverage.py $version by <code>pytest --cov=src</code>. Regenerate with
      <code>python scripts/generate_reports.py</code>.
    </p>
  </body>
</html>
"""
)

ROW = "        <tr><td>{name}</td><td>{statements}</td><td>{missed}</td><td>{percent}</td><td>{lines}</td></tr>"


def percent(summary):
    """Format a coverage summary as a percentage with one decimal."""
    return f"{summary['percent_covered']:.1f}%"


def coverage_page(coverage, tests):
    """Render the coverage.py JSON report as an HTML page."""
    rows = []
    for path, measured in sorted(coverage["files"].items()):
        summary = measured["summary"]
        rows.append(
            ROW.format(
                name=html.escape(path.replace("\\", "/")),
                statements=summary["num_statements"],
                missed=summary["missing_lines"],
                percent=percent(summary),
                lines=", ".join(str(line) for line in measured["missing_lines"]) or "-",
            )
        )
    totals = coverage["totals"]
    return PAGE.substitute(
        total_percent=percent(totals),
        tests=html.escape(tests),
        rows="\n".join(rows),
        statements=totals["num_statements"],
        missed=totals["missing_lines"],
        version=coverage["meta"]["version"],
    )


def main():
    """Run the suite once and write both files; exit with pytest's exit code."""
    # --no-header leaves the local folder path out of the saved output.
    command = [sys.executable, "-m", "pytest", "-v", "--no-header", "-p", "no:cacheprovider"]
    command += ["--cov=src", "--cov-report=term-missing", "--cov-report=json"]
    run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)

    json_report = ROOT / "coverage.json"
    coverage = json.loads(json_report.read_text(encoding="utf-8"))
    json_report.unlink()

    # The last line of pytest's output is the verdict, e.g. "==== 103 passed in 0.52s ===="
    verdict = run.stdout.strip().splitlines()[-1].strip("= ")
    lines = [line.rstrip() for line in run.stdout.splitlines()]

    (ROOT / "test_results.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    (ROOT / "coverage_report.html").write_text(
        coverage_page(coverage, verdict), encoding="utf-8", newline="\n"
    )
    print(verdict)
    return run.returncode


if __name__ == "__main__":
    sys.exit(main())
