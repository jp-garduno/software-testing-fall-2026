#!/usr/bin/env python3
"""Count code lines, ignoring blank lines, comments and Python docstrings."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GROUPS = {
    "Page object": (["selenium/pages/todo_page.py"], ["playwright/pages/TodoPage.js"]),
    "CRUD and editing tests": (["selenium/tests/test_todo_crud.py"], ["playwright/tests/todo-crud.spec.js"]),
    "Filter tests": (["selenium/tests/test_todo_filter.py"], ["playwright/tests/todo-filter.spec.js"]),
    "Setup and configuration": (
        ["selenium/pages/browser.py", "selenium/tests/conftest.py", "selenium/pytest.ini"],
        ["playwright/config/target.js", "playwright/playwright.config.js"],
    ),
}


def code_lines(path):
    text = (ROOT / path).read_text()
    skip = set()
    if path.endswith(".py"):
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)) and ast.get_docstring(node):
                skip.update(range(node.body[0].lineno, node.body[0].end_lineno + 1))
    count = 0
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped and number not in skip and not stripped.startswith(("#", "//", "/*", "*")):
            count += 1
    return count


def main():
    print("| Component | Selenium (Python) | Playwright (JavaScript) |")
    print("| --- | ---: | ---: |")
    totals = [0, 0]
    for name, files in GROUPS.items():
        counts = [sum(code_lines(f) for f in side) for side in files]
        if name == "Setup and configuration":
            # Only the e2e project counts: leave out the bonus projects in the config.
            config = (ROOT / "playwright/playwright.config.js").read_text()
            if "name: 'visual'" in config:
                start = config.index("    {\n      name: 'visual'")
                end = config.index("  ],\n});")
                counts[1] -= len([l for l in config[start:end].splitlines()
                                  if l.strip() and not l.strip().startswith("//")])
        totals = [t + c for t, c in zip(totals, counts)]
        print(f"| {name} | {counts[0]} | {counts[1]} |")
    print(f"| **Total** | **{totals[0]}** | **{totals[1]}** |")


if __name__ == "__main__":
    main()
