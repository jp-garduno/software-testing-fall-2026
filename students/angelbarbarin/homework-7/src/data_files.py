"""Loading and validation of the external test-data files.

The tests never hard-code data: they call the loaders below, which turn each CSV row / JSON
object into a ready-to-use case. Before that, the ``validate_*`` functions (bonus option C)
check the files and report every problem with its line number, so a typo in the data is
reported as a data error instead of showing up as a confusing test failure.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

ORDER_COLUMNS = (
    "test_name",
    "category",
    "items",
    "customer_type",
    "discount_code",
    "distance_km",
    "is_express",
    "expected_subtotal",
    "expected_discount",
    "expected_tax",
    "expected_shipping",
    "expected_total",
    "expected_error",
)
EXPECTED_MONEY = ("expected_subtotal", "expected_discount", "expected_tax", "expected_shipping", "expected_total")
ITEM_FIELDS = ("name", "price", "quantity", "weight")
NO_CODE = "NONE"


@dataclass(frozen=True)
class DataError:
    """One problem found in a data file."""

    file: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.file}:{self.line}: {self.message}"


class TestDataError(ValueError):
    """Raised by the loaders when a data file does not pass validation."""

    __test__ = False  # tell pytest this is not a test class


# ---------------------------------------------------------------------- #
# Order calculations (CSV)
# ---------------------------------------------------------------------- #
def _is_float(text: str) -> bool:
    try:
        float(text)
    except (TypeError, ValueError):
        return False
    return True


def _check_items(raw: str) -> Optional[str]:
    """Return a problem description for the items column, or None when it is fine."""
    try:
        items = json.loads(raw)
    except json.JSONDecodeError as exc:
        return f"items is not valid JSON ({exc.msg})"
    if not isinstance(items, list):
        return "items must be a JSON list"
    for index, item in enumerate(items):
        missing = [name for name in ITEM_FIELDS if not isinstance(item, dict) or name not in item]
        if missing:
            return f"item {index} is missing {', '.join(missing)}"
    return None


def _check_order_row(row: Dict[str, str]) -> List[str]:
    """All problems of one CSV row (the column set was already checked)."""
    problems = []
    if not row["test_name"].strip():
        problems.append("test_name is empty")
    items_problem = _check_items(row["items"])
    if items_problem:
        problems.append(items_problem)
    if row["customer_type"] not in ("new", "regular"):
        problems.append(f"customer_type must be new or regular, got {row['customer_type']!r}")
    if not row["discount_code"].strip():
        problems.append(f"discount_code is empty (use {NO_CODE})")
    if not _is_float(row["distance_km"]):
        problems.append(f"distance_km is not a number: {row['distance_km']!r}")
    if row["is_express"] not in ("true", "false"):
        problems.append(f"is_express must be true or false, got {row['is_express']!r}")
    if row["expected_error"].strip():
        if any(row[column].strip() for column in EXPECTED_MONEY):
            problems.append("a row with expected_error must leave the expected amounts empty")
    else:
        problems.extend(
            f"{column} is not a number: {row[column]!r}" for column in EXPECTED_MONEY if not _is_float(row[column])
        )
    return problems


def validate_order_csv(path: Path) -> List[DataError]:
    """Check columns, types, JSON items and duplicate names. Line numbers count the header as line 1."""
    path = Path(path)
    errors: List[DataError] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in ORDER_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            return [DataError(path.name, 1, f"missing column(s): {', '.join(missing)}")]
        seen: Dict[str, int] = {}
        for row in reader:
            line = reader.line_num
            if None in row.values() or None in row:
                errors.append(DataError(path.name, line, "wrong number of columns"))
                continue
            errors.extend(DataError(path.name, line, problem) for problem in _check_order_row(row))
            name = row["test_name"]
            if name in seen:
                errors.append(DataError(path.name, line, f"duplicate test_name {name!r} (first on line {seen[name]})"))
            seen.setdefault(name, line)
    return errors


def load_order_cases(path: Path) -> List[Dict[str, Any]]:
    """Validate and parse the order CSV into dicts with Python types."""
    errors = validate_order_csv(path)
    if errors:
        raise TestDataError("\n".join(str(error) for error in errors))
    cases = []
    with Path(path).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            failing = bool(row["expected_error"].strip())
            cases.append(
                {
                    "test_name": row["test_name"],
                    "category": row["category"],
                    "items": json.loads(row["items"]),
                    "customer_type": row["customer_type"],
                    "discount_code": None if row["discount_code"] == NO_CODE else row["discount_code"],
                    "distance_km": float(row["distance_km"]),
                    "is_express": row["is_express"] == "true",
                    "expected": (
                        None if failing else {c.removeprefix("expected_"): float(row[c]) for c in EXPECTED_MONEY}
                    ),
                    "expected_error": row["expected_error"] or None,
                }
            )
    return cases


# ---------------------------------------------------------------------- #
# JSON files
# ---------------------------------------------------------------------- #
def _json_line_finder(text: str):
    """Approximate the line of each test entry by finding its name in the raw text."""

    def find(name: str) -> int:
        position = text.find(f'"{name}"')
        return text.count("\n", 0, position) + 1 if position >= 0 else 1

    return find


def _read_json(path: Path):
    text = Path(path).read_text(encoding="utf-8")
    try:
        return json.loads(text), text, None
    except json.JSONDecodeError as exc:
        return None, text, DataError(Path(path).name, exc.lineno, f"invalid JSON: {exc.msg}")


def validate_customer_json(path: Path) -> List[DataError]:
    """Each case needs test_name, a customer object and expected.is_valid / expected.errors that agree."""
    path = Path(path)
    data, text, error = _read_json(path)
    if error:
        return [error]
    if not isinstance(data, list):
        return [DataError(path.name, 1, "top level must be a list of cases")]
    line_of = _json_line_finder(text)
    errors = []
    names = set()
    for index, case in enumerate(data):
        name = case.get("test_name") if isinstance(case, dict) else None
        line = line_of(name) if name else 1
        if not name:
            errors.append(DataError(path.name, line, f"case {index} has no test_name"))
            continue
        if name in names:
            errors.append(DataError(path.name, line, f"duplicate test_name {name!r}"))
        names.add(name)
        if not isinstance(case.get("customer"), dict):
            errors.append(DataError(path.name, line, f"{name}: customer must be an object"))
        expected = case.get("expected")
        if not isinstance(expected, dict) or not isinstance(expected.get("is_valid"), bool):
            errors.append(DataError(path.name, line, f"{name}: expected.is_valid must be true or false"))
        elif not isinstance(expected.get("errors"), list):
            errors.append(DataError(path.name, line, f"{name}: expected.errors must be a list"))
        elif expected["is_valid"] == bool(expected["errors"]):
            errors.append(DataError(path.name, line, f"{name}: is_valid contradicts the errors list"))
    return errors


def load_customer_cases(path: Path) -> List[Dict[str, Any]]:
    errors = validate_customer_json(path)
    if errors:
        raise TestDataError("\n".join(str(error) for error in errors))
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_workflow_json(path: Path) -> List[DataError]:
    """Each workflow needs a name and steps; each step an action and an expected object."""
    path = Path(path)
    data, text, error = _read_json(path)
    if error:
        return [error]
    if not isinstance(data, dict) or not isinstance(data.get("workflows"), list):
        return [DataError(path.name, 1, 'top level must be an object with a "workflows" list')]
    line_of = _json_line_finder(text)
    errors = []
    for index, workflow in enumerate(data["workflows"]):
        name = workflow.get("name") if isinstance(workflow, dict) else None
        if not name:
            errors.append(DataError(path.name, 1, f"workflow {index} has no name"))
            continue
        steps = workflow.get("steps")
        if not isinstance(steps, list) or not steps:
            errors.append(DataError(path.name, line_of(name), f"{name}: steps must be a non-empty list"))
            continue
        for number, step in enumerate(steps, start=1):
            if not isinstance(step, dict) or not isinstance(step.get("action"), str):
                errors.append(DataError(path.name, line_of(name), f"{name}: step {number} has no action"))
            elif not isinstance(step.get("expected"), dict):
                errors.append(DataError(path.name, line_of(name), f"{name}: step {number} has no expected object"))
    return errors


def load_workflows(path: Path) -> Dict[str, Any]:
    errors = validate_workflow_json(path)
    if errors:
        raise TestDataError("\n".join(str(error) for error in errors))
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_directory(directory: Path) -> List[DataError]:
    """Validate every known data file that exists in a directory."""
    directory = Path(directory)
    errors: List[DataError] = []
    for csv_file in sorted(directory.glob("*.csv")):
        errors.extend(validate_order_csv(csv_file))
    if (directory / "customer_validation.json").exists():
        errors.extend(validate_customer_json(directory / "customer_validation.json"))
    if (directory / "order_workflows.json").exists():
        errors.extend(validate_workflow_json(directory / "order_workflows.json"))
    return errors


def main(argv: Optional[List[str]] = None) -> int:
    """CLI: ``python src/data_files.py test_data`` prints every problem and exits 1 if any."""
    import sys  # pylint: disable=import-outside-toplevel

    args = sys.argv[1:] if argv is None else argv
    errors = validate_directory(Path(args[0] if args else "test_data"))
    for error in errors:
        print(error)
    print(f"{len(errors)} problem(s) found")
    return 1 if errors else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
