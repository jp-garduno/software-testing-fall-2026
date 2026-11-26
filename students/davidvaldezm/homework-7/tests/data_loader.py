"""Load and validate test data before pytest collects the cases."""

import csv
import json
import math
import re
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import best_match

from tests.data_schemas import CUSTOMER_CASE, ORDER_CASE, WORKFLOW

DATA_DIR = Path(__file__).resolve().parents[1] / "test_data"
FORMAT_CHECKER = FormatChecker()
WHITESPACE = re.compile(r"\s*")


def _fail(path, line, message):
    raise ValueError(f"{path.name}:{line}: {message}")


def _validate(path, line, record, schema):
    errors = Draft202012Validator(schema, format_checker=FORMAT_CHECKER).iter_errors(
        record
    )
    error = best_match(errors)
    if error is not None:
        field = "/".join(map(str, error.absolute_path))
        _fail(path, line, f"{field or 'record'}: {error.message}")


def _bool(value):
    return {"true": True, "false": False}[value]


def _optional_bool(value):
    return _bool(value) if value else None


def _number(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("expected a finite number")
    return result


def _optional_number(value):
    return _number(value) if value else None


def _read_row(path, line, row):
    parsers = {
        "items": json.loads,
        "distance_km": _number,
        "is_express": _bool,
        "discount_applied": _optional_bool,
        **{
            key: _optional_number
            for key in ORDER_CASE["required"]
            if key.startswith("expected_") and key != "expected_error"
        },
    }
    if None in row or None in row.values():
        _fail(path, line, "row has a different number of columns than the header")
    for field, parser in parsers.items():
        try:
            row[field] = parser(row[field])
        except (ValueError, KeyError) as error:
            raise ValueError(f"{path.name}:{line}: {field}: {error}") from error
    row["discount_code"] = (
        None if row["discount_code"] == "NONE" else row["discount_code"]
    )
    row["expected_error"] = row["expected_error"] or None
    _validate(path, line, row, ORDER_CASE)
    return row


def _case(path, line, row, name_key, seen):
    name = row[name_key]
    if name in seen:
        _fail(path, line, f"duplicate case name {name!r}")
    seen.add(name)
    return pytest.param(row, id=name)


def order_cases(filename):
    """Read CSV records and report data errors at the first line of each row."""
    path = DATA_DIR / filename
    cases = []
    seen = set()
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        line = 1
        try:
            columns = reader.fieldnames
            if columns is None or sorted(columns) != sorted(ORDER_CASE["required"]):
                _fail(path, 1, "unexpected CSV header")
            while True:
                line = reader.line_num + 1
                row = next(reader, None)
                if row is None:
                    break
                line = reader.line_num - sum(
                    value.count("\n")
                    for value in row.values()
                    if isinstance(value, str)
                )
                row = _read_row(path, line, row)
                cases.append(_case(path, line, row, "test_name", seen))
        except csv.Error as error:
            raise ValueError(f"{path.name}:{line}: {error}") from error
    if not cases:
        _fail(path, 1, "expected at least one CSV case")
    return cases


def _json_array_cases(path, source, start, schema, name_key):
    decoder = json.JSONDecoder()
    seen = set()
    cases = []
    index = WHITESPACE.match(source, start + 1).end()
    # The whole document has already parsed, so only a comma or ] can follow a record.
    while source[index] != "]":
        line = source.count("\n", 0, index) + 1
        row, end = decoder.raw_decode(source, index)
        _validate(path, line, row, schema)
        cases.append(_case(path, line, row, name_key, seen))
        index = WHITESPACE.match(source, end).end()
        if source[index] == ",":
            index = WHITESPACE.match(source, index + 1).end()
    if not cases:
        _fail(path, source.count("\n", 0, start) + 1, "expected at least one JSON case")
    return cases


def json_cases(filename, *, workflows=False):
    """Read JSON records and report syntax or schema errors with source lines."""
    path = DATA_DIR / filename
    source = path.read_text(encoding="utf-8")
    try:
        data = json.loads(source)
    except json.JSONDecodeError as error:
        raise ValueError(f"{path.name}:{error.lineno}: {error.msg}") from error
    if workflows:
        if not isinstance(data, dict) or list(data) != ["workflows"]:
            _fail(path, 1, "expected an object containing only a workflows array")
        match = re.match(r'\s*\{\s*"(?:[^"\\]|\\.)*"\s*:\s*\[', source)
        if not isinstance(data["workflows"], list) or match is None:
            _fail(path, 1, "expected a workflows array")
        return _json_array_cases(path, source, match.end() - 1, WORKFLOW, "name")
    if not isinstance(data, list):
        _fail(path, 1, "expected a customer case array")
    return _json_array_cases(
        path, source, source.index("["), CUSTOMER_CASE, "test_name"
    )
