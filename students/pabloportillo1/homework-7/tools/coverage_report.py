"""Write coverage_report.html, one self-contained page summarising the last coverage run.

Run ``python -m pytest --cov=src --cov-branch`` and then ``python -m tools.coverage_report``. coverage.py's own
HTML report is a folder of pages with generated JavaScript, which the grading workflow would lint as if it were
submission code, so this page is built from coverage.py's JSON data instead.
"""

import json
import tempfile
from html import escape
from pathlib import Path

import coverage

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / ".coverage"
OUTPUT = ROOT / "coverage_report.html"
STYLE = """
:root { --bg: #ffffff; --fg: #1f2328; --muted: #59636e; --line: #d1d9e0; --head: #f6f8fa; --ok: #1a7f37; --bad: #cf222e; }
@media (prefers-color-scheme: dark) {
  :root { --bg: #0d1117; --fg: #e6edf3; --muted: #9198a1; --line: #3d444d; --head: #151b23; --ok: #3fb950; --bad: #f85149; }
}
body { margin: 0; padding: 32px 16px; background: var(--bg); color: var(--fg); font: 15px/1.5 system-ui, sans-serif; }
main { max-width: 960px; margin: 0 auto; }
h1 { margin: 0 0 4px; font-size: 24px; }
p { margin: 0 0 24px; color: var(--muted); }
.table { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
th, td { padding: 8px 12px; border-bottom: 1px solid var(--line); text-align: right; white-space: nowrap; }
th:first-child, td:first-child, td.missing { text-align: left; }
thead th { background: var(--head); font-weight: 600; }
tfoot td { font-weight: 600; }
.full { color: var(--ok); }
.partial { color: var(--bad); }
"""


def build_report(data_file=DATA_FILE, output=OUTPUT):
    measured = coverage.Coverage(data_file=str(data_file))
    measured.load()
    with tempfile.TemporaryDirectory() as directory:
        json_path = Path(directory) / "coverage.json"
        measured.json_report(outfile=str(json_path))
        data = json.loads(json_path.read_text(encoding="utf-8"))
    output.write_text(render(data), encoding="utf-8")
    return data["totals"]["percent_covered"]


def render(data):
    rows = "".join(
        _row(escape(name), details["summary"], ", ".join(map(str, details["missing_lines"])) or "-")
        for name, details in sorted(data["files"].items())
    )
    total = _row("Total", data["totals"], "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Homework 7 Coverage</title>
<style>{STYLE}</style>
</head>
<body>
<main>
<h1>Homework 7 coverage: {data["totals"]["percent_covered_display"]}%</h1>
<p>Statement and branch coverage of <code>src/</code>, measured with coverage.py {escape(data["meta"]["version"])}
on {escape(data["meta"]["timestamp"][:10])}.</p>
<div class="table">
<table>
<thead><tr><th>File</th><th>Statements</th><th>Missed</th><th>Branches</th><th>Partial</th><th>Coverage</th>
<th>Missing lines</th></tr></thead>
<tbody>{rows}</tbody>
<tfoot>{total}</tfoot>
</table>
</div>
</main>
</body>
</html>
"""


def _row(name, summary, missing_lines):
    percent = summary["percent_covered"]
    status = "full" if percent == 100 else "partial"
    return (
        f"<tr><td>{name}</td><td>{summary['num_statements']}</td><td>{summary['missing_lines']}</td>"
        f"<td>{summary.get('num_branches', 0)}</td><td>{summary.get('num_partial_branches', 0)}</td>"
        f"<td class=\"{status}\">{summary['percent_covered_display']}%</td>"
        f'<td class="missing">{escape(missing_lines)}</td></tr>'
    )


def main():
    percent = build_report()
    print(f"Wrote {OUTPUT.name}: {percent:.2f}% covered")


if __name__ == "__main__":
    main()
