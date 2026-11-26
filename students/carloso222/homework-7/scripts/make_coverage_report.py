"""Build a single self-contained coverage_report.html from the htmlcov/ index (CSS inlined).

Usage (from the homework-7 folder):
    python -m pytest --cov=src --cov-report=html:htmlcov
    python scripts/make_coverage_report.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTMLCOV = ROOT / "htmlcov"


def build_report() -> Path:
    """Inline the stylesheet into htmlcov/index.html and write coverage_report.html."""
    html = (HTMLCOV / "index.html").read_text(encoding="utf-8")
    for href in re.findall(r'<link rel="stylesheet" href="([^"]+\.css)"[^>]*>', html):
        css = (HTMLCOV / href).read_text(encoding="utf-8")
        html = re.sub(
            rf'<link rel="stylesheet" href="{re.escape(href)}"[^>]*>',
            lambda _, css=css: f"<style>{css}</style>",
            html,
        )
    target = ROOT / "coverage_report.html"
    target.write_text(html, encoding="utf-8")
    return target


if __name__ == "__main__":
    print(f"Wrote {build_report()}")
