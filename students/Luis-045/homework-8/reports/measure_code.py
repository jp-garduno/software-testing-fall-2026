"""Reproduce LOC and cyclomatic complexity for equivalent page objects and tests."""

import ast
import json
import subprocess
from pathlib import Path

from mccabe import PathGraphingAstVisitor

ROOT = Path(__file__).resolve().parents[1]
PYTHON_FILES = [
    "selenium/pages/todo_page.py",
    "selenium/tests/test_todo_crud.py",
    "selenium/tests/test_todo_filter.py",
]
JS_METRICS = """
const fs = require("node:fs");
const { Linter } = require("eslint");
const linter = new Linter();
const files = ["pages/TodoPage.js", "tests/todo-crud.spec.js", "tests/todo-filter.spec.js"];
const result = {};
for (const file of files) {
  const source = fs.readFileSync(file, "utf8");
  const functions = linter.verify(source, {
    parserOptions: { ecmaVersion: 2022 },
    rules: { complexity: ["warn", 0] },
  }).map((item) => ({
    line: item.line,
    complexity: Number(item.message.match(/complexity of ([0-9]+)/)[1]),
  }));
  result["playwright/" + file] = {
    physical_lines: source.trimEnd().split("\\n").length,
    functions,
  };
}
process.stdout.write(JSON.stringify(result));
"""


def measure_python(filename):
    """Use mccabe's AST graphs, without importing or executing the test code."""
    source = (ROOT / filename).read_text(encoding="utf-8")
    visitor = PathGraphingAstVisitor()
    visitor.preorder(ast.parse(source), visitor)
    return {
        "physical_lines": len(source.splitlines()),
        "functions": [
            {"name": name, "complexity": graph.complexity()}
            for name, graph in visitor.graphs.items()
        ],
    }


def main():
    """Write raw per-file data and aggregate the two equivalent implementations."""
    python = {filename: measure_python(filename) for filename in PYTHON_FILES}
    completed = subprocess.run(
        ["node", "-e", JS_METRICS],
        cwd=ROOT / "playwright",
        check=True,
        capture_output=True,
        text=True,
    )
    javascript = json.loads(completed.stdout)
    results = {
        "tools": {"python": "mccabe 0.7.0", "javascript": "ESLint 8.57.1 complexity"}
    }
    for name, files in (("selenium", python), ("playwright", javascript)):
        complexity = [
            function["complexity"]
            for file in files.values()
            for function in file["functions"]
        ]
        results[name] = {
            "physical_lines": sum(file["physical_lines"] for file in files.values()),
            "function_count": len(complexity),
            "average_complexity": sum(complexity) / len(complexity),
            "maximum_complexity": max(complexity),
            "files": files,
        }
    output = ROOT / "reports" / "code-metrics.json"
    output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    for name in ("selenium", "playwright"):
        print(
            name, {key: value for key, value in results[name].items() if key != "files"}
        )


if __name__ == "__main__":
    main()
