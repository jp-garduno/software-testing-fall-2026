"""Build the single-file coverage_report.html required by the assignment.

coverage.py writes its HTML report as a folder of many files. This script reads the JSON report
instead and produces one self-contained page with the summary table and the annotated source of
every module (green = executed, red = missed), which is easy to commit and open in a browser.

    pytest --cov=src --cov-branch --cov-report=json
    python tools/coverage_report.py              # coverage.json -> coverage_report.html
"""

from __future__ import annotations

import html
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STYLE = """
body { font-family: system-ui, sans-serif; margin: 24px; color: #1f2328; background: #fff; }
h1 { font-size: 22px; } h2 { font-size: 17px; margin-top: 32px; }
table.summary { border-collapse: collapse; margin: 12px 0; }
table.summary td, table.summary th { border: 1px solid #d0d7de; padding: 6px 12px; text-align: right; }
table.summary th:first-child, table.summary td:first-child { text-align: left; }
pre { background: #f6f8fa; border: 1px solid #d0d7de; padding: 8px 0; overflow-x: auto; font-size: 12px; }
.line { display: block; padding: 0 12px; white-space: pre; }
.run { background: #dafbe1; } .miss { background: #ffd7d5; } .partial { background: #fff8c5; }
.num { color: #8c959f; display: inline-block; width: 40px; user-select: none; }
"""


def percent(covered: int, total: int) -> str:
    return f"{100 * covered / total:.1f}%" if total else "100.0%"


def summary_row(name: str, summary: dict) -> str:
    cells = [
        html.escape(name),
        summary["num_statements"],
        summary["missing_lines"],
        summary.get("num_branches", 0),
        summary.get("num_partial_branches", 0),
        f"{summary['percent_covered']:.1f}%",
    ]
    return "<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>"


def annotated_source(path: Path, data: dict) -> str:
    executed, missing = set(data["executed_lines"]), set(data["missing_lines"])
    partial = {branch[0] for branch in data.get("missing_branches", [])}
    lines = []
    for number, text in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        css = "partial" if number in partial else "miss" if number in missing else "run" if number in executed else ""
        lines.append(f'<span class="line {css}"><span class="num">{number}</span>{html.escape(text)}</span>')
    return "<pre>" + "".join(lines) + "</pre>"


def build(report: dict) -> str:
    totals = report["totals"]
    rows = "".join(summary_row(name, data["summary"]) for name, data in sorted(report["files"].items()))
    sources = "".join(
        f"<h2>{html.escape(name)} - {data['summary']['percent_covered']:.1f}%</h2>"
        + annotated_source(ROOT / name, data)
        for name, data in sorted(report["files"].items())
    )
    statements = percent(totals["covered_lines"], totals["num_statements"])
    branches = percent(totals.get("covered_branches", 0), totals.get("num_branches", 0))
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Coverage report - homework 7</title>
<style>{STYLE}</style></head><body>
<h1>Coverage report - Homework 7 (data-driven testing)</h1>
<p>Statements: <b>{statements}</b> &middot; Branches: <b>{branches}</b> &middot;
Combined: <b>{totals['percent_covered']:.1f}%</b> &middot; generated {generated} with coverage.py
{html.escape(report['meta']['version'])}</p>
<table class="summary"><tr><th>File</th><th>Statements</th><th>Missing</th><th>Branches</th>
<th>Partial</th><th>Coverage</th></tr>{rows}{summary_row('TOTAL', totals)}</table>
<p><span class="line run" style="display:inline">executed</span>
<span class="line miss" style="display:inline">missed</span>
<span class="line partial" style="display:inline">branch not fully taken</span></p>
{sources}</body></html>
"""


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "coverage.json"
    target = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "coverage_report.html"
    target.write_text(build(json.loads(source.read_text(encoding="utf-8"))), encoding="utf-8")
    print(f"Wrote {target}")


if __name__ == "__main__":
    main()
