"""Load the external test data files into typed test cases.

Every loader validates its file first (see ``data_validation``) and raises
``DataFileError`` listing each problem with its line number, so a broken data
file stops the run at collection time with a message that says where to look.
"""

import csv
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

from src.data_validation import (DATA_DIR, EXPECTED_AMOUNTS, DataIssue, validate_customer_json, validate_order_csv,
                                 validate_workflows_json)


class DataFileError(Exception):
    """A test data file failed validation."""

    def __init__(self, issues: List[DataIssue]):
        self.issues = issues
        super().__init__("Invalid test data:\n" + "\n".join(f"  {issue}" for issue in issues))


@dataclass(frozen=True)
class OrderCase:  # pylint: disable=too-many-instance-attributes  # one attribute per CSV column
    """One row of order_calculations.csv."""

    test_name: str
    category: str
    items: List[Dict]
    customer_type: str
    discount_code: Optional[str]
    distance_km: float
    is_express: bool
    expected: Optional[Dict[str, float]] = None
    expected_error: Optional[str] = None


@dataclass(frozen=True)
class CustomerCase:
    """One entry of customer_validation.json."""

    test_name: str
    category: str
    customer: Dict
    expected_valid: bool
    expected_errors: List[str]
    reference_date: Optional[date] = None
    description: str = ""


@dataclass(frozen=True)
class Workflow:
    """One end-to-end scenario of order_workflows.json."""

    name: str
    steps: List[Dict]
    description: str = ""
    reference_date: Optional[date] = None


def _raise_on(issues: List[DataIssue]) -> None:
    if issues:
        raise DataFileError(issues)


def parse_items(raw: str) -> List[Dict]:
    """Items are written as JSON with single quotes to keep the CSV readable."""
    return json.loads(raw.replace("'", '"'))


def _order_case(row: Dict[str, str]) -> OrderCase:
    error = row["expected_error"].strip() or None
    expected = None if error else {column.removeprefix("expected_"): float(row[column]) for column in EXPECTED_AMOUNTS}
    return OrderCase(
        test_name=row["test_name"],
        category=row["category"],
        items=parse_items(row["items"]),
        customer_type=row["customer_type"],
        discount_code=None if row["discount_code"] == "NONE" else row["discount_code"],
        distance_km=float(row["distance_km"]),
        is_express=row["is_express"] == "true",
        expected=expected,
        expected_error=error,
    )


def load_order_cases(path: Path = DATA_DIR / "order_calculations.csv",
                     category: Optional[str] = None) -> List[OrderCase]:
    """Load order calculation cases, optionally only one category."""
    _raise_on(validate_order_csv(path))
    with open(path, newline="", encoding="utf-8") as handle:
        cases = [_order_case(row) for row in csv.DictReader(handle)]
    return [case for case in cases if category is None or case.category == category]


def load_customer_cases(path: Path = DATA_DIR / "customer_validation.json") -> List[CustomerCase]:
    """Load customer validation cases."""
    _raise_on(validate_customer_json(path))
    with open(path, encoding="utf-8") as handle:
        raw_cases = json.load(handle)
    return [
        CustomerCase(
            test_name=case["test_name"],
            category=case["category"],
            customer=case["customer"],
            expected_valid=case["expected"]["is_valid"],
            expected_errors=case["expected"]["errors"],
            reference_date=date.fromisoformat(case["reference_date"]) if "reference_date" in case else None,
            description=case.get("description", ""),
        )
        for case in raw_cases
    ]


def load_workflows(path: Path = DATA_DIR / "order_workflows.json") -> List[Workflow]:
    """Load the end-to-end workflows."""
    _raise_on(validate_workflows_json(path))
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    reference = date.fromisoformat(data["reference_date"]) if "reference_date" in data else None
    return [
        Workflow(name=workflow["name"], steps=workflow["steps"], description=workflow.get("description", ""),
                 reference_date=reference)
        for workflow in data["workflows"]
    ]
