"""Load external fixtures and report schema problems with source locations."""

import csv
import json
from pathlib import Path

MONEY_FIELDS = ("subtotal", "discount", "tax", "shipping", "total")
CSV_FIELDS = {
    "test_name",
    "category",
    "items",
    "customer_type",
    "discount_code",
    "distance_km",
    "is_express",
    "expected_error",
    *(f"expected_{field}" for field in MONEY_FIELDS),
}


def require(condition, path, line, message):
    """Fail immediately with the fixture file and physical line number."""
    if not condition:
        raise ValueError(f"{path}:{line}: {message}")


def load_orders(path):
    """Validate CSV columns, JSON items and typed expected values before tests."""
    path = Path(path)
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        require(
            CSV_FIELDS.issubset(reader.fieldnames or []), path, 1, "Missing CSV columns"
        )
        rows = []
        names = set()
        for row in reader:
            line = reader.line_num
            require(
                row.get("test_name") and row["test_name"] not in names,
                path,
                line,
                "Missing or duplicate test_name",
            )
            names.add(row["test_name"])
            try:
                items = json.loads(row["items"])
                float(row["distance_km"])
                for field in MONEY_FIELDS:
                    if row["expected_error"] == "":
                        float(row[f"expected_{field}"])
            except (ValueError, TypeError) as error:
                raise ValueError(
                    f"{path}:{line}: Invalid JSON or numeric field"
                ) from error
            require(isinstance(items, list), path, line, "items must be a list")
            for item in items:
                require(
                    isinstance(item, dict) and isinstance(item.get("name"), str),
                    path,
                    line,
                    "Invalid item name",
                )
                for field in ("price", "quantity", "weight"):
                    value = item.get(field)
                    require(
                        isinstance(value, (int, float)) and not isinstance(value, bool),
                        path,
                        line,
                        f"Invalid item {field} type",
                    )
                require(
                    isinstance(item["quantity"], int),
                    path,
                    line,
                    "quantity must be integer",
                )
            require(
                row["is_express"] in ("true", "false"),
                path,
                line,
                "is_express must be true/false",
            )
            require(
                row["customer_type"] in ("new", "regular"),
                path,
                line,
                "Invalid customer_type",
            )
            require(
                row["expected_error"] in ("", "ValueError"),
                path,
                line,
                "Unsupported expected_error",
            )
            rows.append(row)
    require(bool(rows), path, 1, "Empty CSV data")
    return rows


def load_json(path):
    """Read JSON while preserving syntax-error line numbers."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError(f"{path}:{error.lineno}: Invalid JSON") from error
    return data, text


def case_line(text, name):
    """Locate a named fixture's opening metadata line."""
    return next(
        (
            index
            for index, line in enumerate(text.splitlines(), 1)
            if json.dumps(name) in line
        ),
        1,
    )


def load_customers(path):
    """Validate envelope and oracle types, allowing intentional invalid inputs."""
    data, text = load_json(path)
    require(
        isinstance(data, list) and bool(data), path, 1, "Expected nonempty case list"
    )
    names = set()
    for case in data:
        require(isinstance(case, dict), path, 1, "Case must be an object")
        name = case.get("test_name")
        line = case_line(text, name)
        require(
            isinstance(name, str) and name and name not in names,
            path,
            line,
            "Invalid or duplicate test_name",
        )
        names.add(name)
        require(
            isinstance(case.get("customer"), dict),
            path,
            line,
            "customer must be an object",
        )
        expected = case.get("expected", {})
        require(
            isinstance(expected, dict) and isinstance(expected.get("is_valid"), bool),
            path,
            line,
            "is_valid must be boolean",
        )
        errors = expected.get("errors")
        require(
            isinstance(errors, list)
            and all(isinstance(error, str) for error in errors),
            path,
            line,
            "errors must be a string list",
        )
        require(
            expected["is_valid"] == (not errors),
            path,
            line,
            "Conflicting expected result",
        )
    return data


def load_workflows(path):
    """Validate workflow actions and their expected output objects."""
    data, text = load_json(path)
    require(
        isinstance(data, dict) and isinstance(data.get("workflows"), list),
        path,
        1,
        "Missing workflows list",
    )
    names = set()
    for flow in data["workflows"]:
        require(isinstance(flow, dict), path, 1, "Workflow must be object")
        name = flow.get("name")
        line = case_line(text, name)
        require(
            isinstance(name, str) and name and name not in names,
            path,
            line,
            "Invalid workflow name",
        )
        names.add(name)
        require(
            isinstance(flow.get("payment_approved"), bool),
            path,
            line,
            "payment_approved must be boolean",
        )
        require(
            isinstance(flow.get("expected_payment_calls"), list),
            path,
            line,
            "Missing payment call expectations",
        )
        steps = flow.get("steps")
        require(
            isinstance(steps, list) and bool(steps),
            path,
            line,
            "Missing workflow steps",
        )
        for step in steps:
            require(
                isinstance(step, dict)
                and step.get("action")
                in {
                    "validate_customer",
                    "create_order",
                    "calculate_total",
                    "process_payment",
                    "confirmation",
                },
                path,
                line,
                "Invalid action",
            )
            require(
                isinstance(step.get("expected"), dict),
                path,
                line,
                "Missing expected object",
            )
    return data
