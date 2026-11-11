"""Bonus C: reject corrupt external fixtures with file and line diagnostics."""

import csv
import json
from pathlib import Path

import pytest

from data_loader import load_orders, load_customers, load_workflows

DATA = Path(__file__).resolve().parents[1] / "test_data"


def test_missing_csv_columns_reports_header_line(tmp_path):
    """Missing field names identify the CSV header."""
    path = tmp_path / "missing.csv"
    path.write_text("test_name,items\na,[]\n", encoding="utf-8")
    with pytest.raises(ValueError, match=r"missing.csv:1: Missing CSV columns"):
        load_orders(path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("items", "not JSON"),
        ("distance_km", "far"),
        ("is_express", "yes"),
        ("expected_total", "unknown"),
    ],
)
def test_invalid_csv_values_report_data_line(tmp_path, field, value):
    """Syntax and value-type failures are located at the data row."""
    rows = load_orders(DATA / "order_calculations.csv")
    row = dict(rows[0])
    row[field] = value
    path = tmp_path / "invalid.csv"
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=row)
        writer.writeheader()
        writer.writerow(row)
    with pytest.raises(ValueError, match=r"invalid.csv:2:"):
        load_orders(path)


def test_invalid_json_reports_syntax_line(tmp_path):
    """A malformed JSON document retains the parser's physical line."""
    path = tmp_path / "broken.json"
    path.write_text('[\n {"test_name": }\n]', encoding="utf-8")
    with pytest.raises(ValueError, match=r"broken.json:2: Invalid JSON"):
        load_customers(path)


def test_wrong_expected_type_reports_named_case_line(tmp_path):
    """A string is_valid is rejected before business tests run."""
    data = load_customers(DATA / "customer_validation.json")[:1]
    data[0]["expected"]["is_valid"] = "true"
    path = tmp_path / "customer.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    with pytest.raises(ValueError, match=r"customer.json:3: is_valid must be boolean"):
        load_customers(path)


def test_unknown_workflow_action_reports_case_line(tmp_path):
    """Unsupported actions cannot silently fall through to confirmation."""
    data = load_workflows(DATA / "order_workflows.json")
    data["workflows"][0]["steps"][0]["action"] = "unknown"
    path = tmp_path / "workflow.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    with pytest.raises(ValueError, match=r"workflow.json:5: Invalid action"):
        load_workflows(path)
