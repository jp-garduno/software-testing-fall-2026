"""
Data Validator Module (Bonus Option C).

Validates test data files (CSV, JSON) for required fields, formats,
and value types before executing data-driven tests.
"""

import csv
import json
import os
from typing import List, Dict


class DataValidationError(Exception):
    """Raised when test data fails schema or integrity validation."""
    pass


def validate_order_calculations_csv(filepath: str) -> List[str]:
    """
    Validate the order calculations CSV file.
    Returns a list of error strings (empty if valid).
    """
    if not os.path.exists(filepath):
        return [f"File not found: {filepath}"]

    errors = []
    required_columns = [
        "test_name", "items", "customer_type", "discount_code",
        "distance_km", "is_express", "expected_subtotal",
        "expected_discount", "expected_tax", "expected_shipping", "expected_total"
    ]

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return ["CSV is empty or missing headers"]

        for col in required_columns:
            if col not in reader.fieldnames:
                errors.append(f"Missing header column: '{col}'")

        if errors:
            return errors

        for line_num, row in enumerate(reader, start=2):
            if not row.get("test_name"):
                errors.append(f"Line {line_num}: Empty 'test_name'")

            # Validate items JSON
            raw_items = row.get("items", "")
            try:
                parsed_items = json.loads(raw_items.replace("'", '"'))
                if not isinstance(parsed_items, list):
                    errors.append(f"Line {line_num}: 'items' must be a JSON array")
                else:
                    for item in parsed_items:
                        for key in ("name", "price", "quantity", "weight"):
                            if key not in item:
                                errors.append(f"Line {line_num}: Item missing key '{key}'")
            except Exception as e:
                errors.append(f"Line {line_num}: Invalid JSON in 'items': {e}")

            # Validate numbers
            for num_col in ("distance_km", "expected_subtotal", "expected_discount",
                            "expected_tax", "expected_shipping", "expected_total"):
                val = row.get(num_col, "")
                try:
                    float(val)
                except ValueError:
                    errors.append(f"Line {line_num}: Field '{num_col}' is not a valid float: '{val}'")

            # Validate boolean
            is_express_val = str(row.get("is_express", "")).strip().lower()
            if is_express_val not in ("true", "false"):
                errors.append(f"Line {line_num}: 'is_express' must be 'true' or 'false', got '{is_express_val}'")

    return errors


def validate_customer_validation_json(filepath: str) -> List[str]:
    """
    Validate the customer validation JSON test data.
    """
    if not os.path.exists(filepath):
        return [f"File not found: {filepath}"]

    errors = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"Invalid JSON syntax in {filepath}: {e}"]

    if not isinstance(data, list):
        return [f"Root of {filepath} must be a list of test cases"]

    for idx, case in enumerate(data, start=1):
        test_name = case.get("test_name", f"case_{idx}")
        if "customer" not in case:
            errors.append(f"Case '{test_name}' missing 'customer' object")
        if "expected" not in case:
            errors.append(f"Case '{test_name}' missing 'expected' object")
        else:
            exp = case["expected"]
            if "is_valid" not in exp or not isinstance(exp["is_valid"], bool):
                errors.append(f"Case '{test_name}' expected.is_valid must be boolean")
            if "errors" not in exp or not isinstance(exp["errors"], list):
                errors.append(f"Case '{test_name}' expected.errors must be list")

    return errors


def validate_order_workflows_json(filepath: str) -> List[str]:
    """
    Validate the order workflows JSON test data.
    """
    if not os.path.exists(filepath):
        return [f"File not found: {filepath}"]

    errors = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"Invalid JSON syntax in {filepath}: {e}"]

    if not isinstance(data, dict) or "workflows" not in data:
        return [f"Root of {filepath} must be an object with a 'workflows' list"]

    workflows = data["workflows"]
    if not isinstance(workflows, list) or len(workflows) < 3:
        errors.append(f"Workflows list must contain at least 3 workflows, found {len(workflows) if isinstance(workflows, list) else 0}")

    for idx, wf in enumerate(workflows, start=1):
        name = wf.get("name", f"workflow_{idx}")
        steps = wf.get("steps")
        if not isinstance(steps, list) or len(steps) == 0:
            errors.append(f"Workflow '{name}' must have a non-empty 'steps' list")

    return errors

