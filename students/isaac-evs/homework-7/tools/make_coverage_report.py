"""Build a self-contained coverage_report.html from coverage.json.

Usage (from the homework-7 directory):
    pytest --cov=src --cov-branch --cov-report=json
    python tools/make_coverage_report.py
"""

import json
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STYLE = """
body{font-family:system-ui,sans-serif;margin:2rem;color:#1f2937}
table{border-collapse:collapse;width:100%;max-width:60rem}
th,td{border:1px solid #d1d5db;padding:.4rem .7rem;text-align:right}
th:first-child,td:first-child{text-align:left}
th{background:#f3f4f6}
.good{color:#15803d;font-weight:600}.bad{color:#b91c1c;font-weight:600}
"""


def percent(covered, total):
    """Percentage as text; a file with nothing to cover counts as 100%."""
    return "100.0%" if total == 0 else f"{100 * covered / total:.1f}%"


def row(name, summary, missing):
    """One table row for a file (or the totals line)."""
    statements, branches = summary["num_statements"], summary.get("num_branches", 0)
    covered = summary["covered_lines"] + summary.get("covered_branches", 0)
    combined = percent(covered, statements + branches)
    css = "good" if combined == "100.0%" or float(combined[:-1]) >= 80 else "bad"
    return (
        f"<tr><td>{escape(name)}</td><td>{statements}</td><td>{summary['missing_lines']}</td><td>{branches}</td>"
        f"<td>{summary.get('missing_branches', 0)}</td><td class='{css}'>{combined}</td>"
        f"<td>{escape(', '.join(map(str, missing)) or '-')}</td></tr>"
    )


def build(data):
    """Return the full HTML document for a coverage.json payload."""
    rows = [row(name, info["summary"], info["missing_lines"]) for name, info in sorted(data["files"].items())]
    rows.append(row("TOTAL", data["totals"], []))
    return (
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><title>Coverage report - homework 7</title>"
        f"<style>{STYLE}</style></head><body><h1>Coverage report</h1>"
        f"<p>Generated {date.today().isoformat()} by <code>pytest --cov=src --cov-branch</code>. "
        "Combined figure = (covered statements + covered branches) / (statements + branches).</p>"
        "<table><tr><th>File</th><th>Statements</th><th>Missed</th><th>Branches</th><th>Missed branches</th>"
        "<th>Coverage</th><th>Missing lines</th></tr>" + "".join(rows) + "</table></body></html>\n"
    )


def main():
    data = json.loads((ROOT / "coverage.json").read_text(encoding="utf-8"))
    (ROOT / "coverage_report.html").write_text(build(data), encoding="utf-8")
    print("wrote coverage_report.html")


if __name__ == "__main__":
    main()
