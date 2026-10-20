"""Summarize measured coverage; run after generating reports/coverage.json."""

import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / "reports/coverage.json").read_text(encoding="utf-8"))
files = {}
for name, details in data["files"].items():
    functions = [info for name, info in details["functions"].items() if name]
    files[name.replace("\\", "/")] = {
        "statements": details["summary"]["num_statements"],
        "covered_statements": details["summary"]["covered_lines"],
        "branches": details["summary"]["num_branches"],
        "covered_branches": details["summary"]["covered_branches"],
        "functions": len(functions),
        "covered_functions": sum(info["summary"]["covered_lines"] > 0 for info in functions),
        "missing_lines": details["missing_lines"],
        "missing_branches": details["missing_branches"],
    }
summary = {
    "measurement": "pytest --cov=src --cov-branch; named Python function bodies from coverage JSON",
    "coverage_version": data["meta"]["version"],
    "totals": data["totals"],
    "functions": sum(info["functions"] for info in files.values()),
    "covered_functions": sum(info["covered_functions"] for info in files.values()),
    "files": files,
}
target = root / "reports/coverage-summary.json"
target.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(target)
