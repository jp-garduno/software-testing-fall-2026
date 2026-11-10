"""Rebuild test_results.txt and the single-file coverage_report.html.

Run from the homework-7 directory:  python scripts/make_reports.py
"""

import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    run = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-v",
            "--cov=src",
            "--cov-report=term-missing",
            "--cov-report=json:.coverage.json",
            "-p",
            "no:cacheprovider",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    (ROOT / "test_results.txt").write_text(run.stdout, encoding="utf-8")
    data = json.loads((ROOT / ".coverage.json").read_text())
    rows = "".join(
        f"<tr><td>{html.escape(name)}</td><td>{f['summary']['num_statements']}</td>"
        f"<td>{f['summary']['missing_lines']}</td><td>{f['summary']['percent_covered']:.1f}%</td>"
        f"<td>{html.escape(', '.join(map(str, f['missing_lines'])) or '-')}</td></tr>"
        for name, f in sorted(data["files"].items())
    )
    total = data["totals"]
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Coverage report - Homework 7</title>
<style>body{{font-family:system-ui,sans-serif;margin:2rem}}table{{border-collapse:collapse}}
td,th{{border:1px solid #bbb;padding:.4rem .8rem;text-align:left}}th{{background:#eee}}</style></head><body>
<h1>Coverage report - Homework 7</h1>
<p>Total: <b>{total['percent_covered']:.1f}%</b> ({total['covered_lines']}/{total['num_statements']} statements)</p>
<table><tr><th>File</th><th>Statements</th><th>Missed</th><th>Cover</th><th>Missing lines</th></tr>{rows}</table>
</body></html>"""
    (ROOT / "coverage_report.html").write_text(page, encoding="utf-8")
    (ROOT / ".coverage.json").unlink()
    print(run.stdout.splitlines()[-1])
    return run.returncode


if __name__ == "__main__":
    sys.exit(main())
