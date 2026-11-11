"""Render a standalone HTML report from the coverage.py JSON export."""

import json
from html import escape
from pathlib import Path

HOMEWORK_DIR = Path(__file__).resolve().parents[1]


def table_row(filename: str, summary: dict, details: dict) -> str:
    """Format counts and uncovered locations for one source file."""
    display_name = escape(filename.replace("\\", "/"))
    lines = ", ".join(map(str, details["missing_lines"])) or "&mdash;"
    branches = ", ".join(
        f"{start}&rarr;{end}" for start, end in details["missing_branches"]
    )
    return (
        "<tr>"
        f'<th scope="row"><code>{display_name}</code></th>'
        f'<td>{summary["covered_lines"]}/{summary["num_statements"]}</td>'
        f'<td>{summary["covered_branches"]}/{summary["num_branches"]}</td>'
        f'<td>{summary["percent_covered"]:.2f}%</td>'
        f"<td>{lines}</td><td>{branches or '&mdash;'}</td>"
        "</tr>"
    )


def main() -> None:
    """Write coverage_report.html next to the submission README."""
    data = json.loads((HOMEWORK_DIR / "coverage.json").read_text(encoding="utf-8"))
    totals = data["totals"]
    rows = "\n".join(
        table_row(filename, details["summary"], details)
        for filename, details in sorted(data["files"].items())
    )
    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Homework 7: reporte de cobertura</title>
<style>
  body {{ margin: 2rem auto; padding: 0 1rem; max-width: 66rem;
          font: 1rem/1.5 system-ui, sans-serif; color: #142739; background: #fff; }}
  table {{ width: 100%; border-collapse: collapse; text-align: left; }}
  th, td {{ padding: .6rem; border-bottom: 1px solid #cbd5e1; vertical-align: top; }}
  thead {{ background: #edf4fa; }}
  code {{ white-space: nowrap; }}
  .table-wrap {{ overflow-x: auto; }}
</style>
</head>
<body>
<main>
<h1>Homework 7: reporte de cobertura</h1>
<p><strong>{totals["percent_covered"]:.2f}% de cobertura combinada en <code>src/</code>.</strong>
   Se ejecutaron {totals["covered_lines"]} de {totals["num_statements"]} sentencias y
   {totals["covered_branches"]} de {totals["num_branches"]} ramas.</p>
<div class="table-wrap">
<table>
<thead><tr><th scope="col">Archivo</th><th scope="col">Sentencias</th>
<th scope="col">Ramas</th><th scope="col">Cobertura</th>
<th scope="col">Líneas sin ejecutar</th><th scope="col">Ramas sin ejecutar</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</div>
<p>Datos de coverage.py {escape(data["meta"]["version"])}. Las columnas de
   sentencias y ramas muestran ejecutadas/total.</p>
</main>
</body>
</html>
"""
    (HOMEWORK_DIR / "coverage_report.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
