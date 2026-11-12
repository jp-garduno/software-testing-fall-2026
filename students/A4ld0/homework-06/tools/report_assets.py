"""Preserve the reviewed coverage.py browser asset when regenerating HTML."""
from hashlib import sha256


def normalize_report_assets(root):
    report = root / "coverage"
    source = root / "tools/coverage_assets/coverage_html.js"
    scripts = list(report.glob("coverage_html_cb_*.js"))
    if not scripts:
        raise RuntimeError("The coverage report has no browser asset to normalize")
    contents = source.read_bytes()
    name = f"coverage_html_cb_{sha256(contents).hexdigest()[:8]}.js"
    target = report / name
    target.write_bytes(contents)
    for page in report.glob("*.html"):
        html = page.read_text(encoding="utf-8")
        for script in scripts:
            html = html.replace(script.name, name)
        page.write_text(html, encoding="utf-8")
    for script in scripts:
        if script != target:
            script.unlink()
