"""Validate every test data file before the tests run (bonus option C)."""

from pathlib import Path
from typing import List

from src.data_checks import DataIssue
from src.json_data_check import validate_customers_json, validate_workflows_json
from src.orders_csv_check import validate_orders_csv

CSV_FILES = ("order_calculations.csv", "generated_orders.csv")
CUSTOMERS_FILE = "customer_validation.json"
WORKFLOWS_FILE = "order_workflows.json"


def validate_all(data_dir: Path) -> List[DataIssue]:
    """Validate all known data files in `data_dir`; a missing required file is reported as an issue."""
    issues: List[DataIssue] = []
    for name in CSV_FILES:
        if (data_dir / name).exists():
            issues += validate_orders_csv(data_dir / name)
    for name, validator in (
        (CUSTOMERS_FILE, validate_customers_json),
        (WORKFLOWS_FILE, validate_workflows_json),
    ):
        if (data_dir / name).exists():
            issues += validator(data_dir / name)
        else:
            issues.append(DataIssue(name, 0, "required data file not found"))
    if not (data_dir / CSV_FILES[0]).exists():
        issues.append(DataIssue(CSV_FILES[0], 0, "required data file not found"))
    return issues


def format_report(issues: List[DataIssue]) -> str:
    """Human-readable report: one 'file:line: message' per issue."""
    header = f"{len(issues)} problem(s) found in the test data files:"
    return "\n".join([header] + [f"  {issue}" for issue in issues])
