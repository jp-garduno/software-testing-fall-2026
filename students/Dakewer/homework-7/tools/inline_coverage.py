"""Turn htmlcov/index.html into one self-contained coverage_report.html.

pytest-cov writes an HTML folder (index.html + css/js + one page per file).
The assignment asks for a single ``coverage_report.html``, so this inlines
the stylesheet and scripts of the index page.
"""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
folder = root / "htmlcov"
html = (folder / "index.html").read_text()


def inline_css(match):
    return f"<style>{(folder / match.group(1)).read_text()}</style>"


def inline_js(match):
    return f"<script>{(folder / match.group(1)).read_text()}</script>"


html = re.sub(r'<link rel="stylesheet" href="([^"]+\.css)"[^>]*>', inline_css, html)
html = re.sub(r'<script src="([^"]+\.js)"[^>]*></script>', inline_js, html)
(root / "coverage_report.html").write_text(html)
print("Wrote coverage_report.html", file=sys.stderr)
