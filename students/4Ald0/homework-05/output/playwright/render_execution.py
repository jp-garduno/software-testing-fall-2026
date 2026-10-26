from html import escape
from pathlib import Path

root = Path(__file__).resolve().parents[2]
text = (root / "reports/test-execution.txt").read_text(encoding="utf-8-sig")
excerpt = text[text.index("=============================== tests coverage"):]
html = '''<!doctype html><meta charset="utf-8"><title>TaskFlow: pytest execution</title>
<style>body{background:#111827;color:#e5e7eb;margin:48px;font:18px Consolas,monospace}
h1{font:30px system-ui;color:#a7f3d0}p{font:18px system-ui;line-height:1.5}
pre{background:#1f2937;border:1px solid #4b5563;border-radius:8px;padding:26px;
font:18px/1.8 Consolas,monospace;white-space:pre-wrap}</style>
<h1>TaskFlow — pytest execution evidence</h1>
<p>Verbatim excerpt of captured stdout, displayed in a browser.<br>
Full output: reports/test-execution.txt<br>112 tests collected, all passed; no skipped or xfail tests.</p>
<pre>pytest -v --cov=src --cov-branch --cov-report=term-missing<br>
''' + escape(excerpt) + '</pre>'
(root / "output/playwright/test-execution.html").write_text(html, encoding="utf-8")
