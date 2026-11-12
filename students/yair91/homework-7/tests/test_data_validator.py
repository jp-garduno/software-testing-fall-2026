"""Tests for the test data validator (bonus, option C).

The broken files are written into tmp_path instead of being committed, so
test_data/ only holds data the suite actually uses.
"""

import json

import pytest

from conftest import DATA_DIR
from data_validator import (
    DataValidationError,
    require_valid_data,
    validate_all,
    validate_customer_json,
    validate_order_csv,
)

HEADER = (
    "test_name,category,items,customer_type,discount_code,distance_km,is_express,"
    "expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total,expected_error"
)
GOOD_ROW = (
    'ok,simple,"[{""name"": ""X"", ""price"": 1.0, ""quantity"": 1, ""weight"": 0.0}]",'
    "regular,NONE,0,false,1.00,0.00,0.08,0.00,1.08,"
)


def write_csv(tmp_path, *rows):
    """Build a temporary CSV with the good header and the given rows."""
    path = tmp_path / "order_calculations.csv"
    path.write_text("\n".join((HEADER,) + rows) + "\n", encoding="utf-8")
    return str(path)


def write_json(tmp_path, content):
    """Build a temporary customer JSON file."""
    path = tmp_path / "customer_validation.json"
    path.write_text(json.dumps(content), encoding="utf-8")
    return str(path)


class TestTheRealDataIsFine:
    """The whole point of the module: warn before the suite runs."""

    def test_the_order_csv_has_no_problems(self):
        assert not validate_order_csv(f"{DATA_DIR}/order_calculations.csv")

    def test_the_customer_json_has_no_problems(self):
        assert not validate_customer_json(f"{DATA_DIR}/customer_validation.json")

    def test_validate_all_checks_both(self):
        findings = validate_all(DATA_DIR)
        assert set(findings) == {"order_calculations.csv", "customer_validation.json"}
        assert all(not problems for problems in findings.values())

    def test_require_valid_data_does_not_raise(self):
        require_valid_data(DATA_DIR)


class TestProblemsInTheCsv:
    """Every problem is reported with file, line and column."""

    def test_a_missing_column(self, tmp_path):
        path = tmp_path / "order_calculations.csv"
        path.write_text("test_name,category\nok,simple\n", encoding="utf-8")
        problems = validate_order_csv(str(path))

        assert len(problems) == 1
        assert "missing columns" in problems[0]
        assert "order_calculations.csv:1" in problems[0]

    def test_a_file_with_no_rows(self, tmp_path):
        problems = validate_order_csv(write_csv(tmp_path))
        assert any("no data rows" in p for p in problems)

    def test_an_empty_name(self, tmp_path):
        row = GOOD_ROW.replace("ok,simple", ",simple", 1)
        problems = validate_order_csv(write_csv(tmp_path, row))
        assert any("[test_name]" in p and "is empty" in p for p in problems)

    def test_a_duplicated_name_names_the_second_line(self, tmp_path):
        problems = validate_order_csv(write_csv(tmp_path, GOOD_ROW, GOOD_ROW))
        assert any(":3" in p and "duplicated" in p for p in problems)

    def test_an_unknown_category(self, tmp_path):
        row = GOOD_ROW.replace("ok,simple", "ok,invented", 1)
        problems = validate_order_csv(write_csv(tmp_path, row))
        assert any("[category]" in p for p in problems)

    def test_a_badly_written_boolean(self, tmp_path):
        row = GOOD_ROW.replace(",NONE,0,false,", ",NONE,0,False,", 1)
        problems = validate_order_csv(write_csv(tmp_path, row))
        assert any("[is_express]" in p for p in problems)

    def test_a_number_that_is_not_a_number(self, tmp_path):
        row = GOOD_ROW.replace(",1.00,0.00,", ",lots,0.00,", 1)
        problems = validate_order_csv(write_csv(tmp_path, row))
        assert any("[expected_subtotal]" in p and "is not a number" in p for p in problems)

    def test_an_empty_amount_with_no_expected_error(self, tmp_path):
        row = GOOD_ROW.replace(",1.00,0.00,0.08,0.00,1.08,", ",,0.00,0.08,0.00,1.08,", 1)
        problems = validate_order_csv(write_csv(tmp_path, row))
        assert any("[expected_subtotal]" in p and "no error is expected" in p for p in problems)

    def test_an_empty_amount_with_an_expected_error_is_fine(self, tmp_path):
        row = GOOD_ROW.replace(",1.00,0.00,0.08,0.00,1.08,", ",,,,,,price must not be negative", 1)
        assert not validate_order_csv(write_csv(tmp_path, row))

    @pytest.mark.parametrize(
        "cell,fragment",
        [
            ("not json", "is not valid JSON"),
            ('"{""a"": 1}"', "must be a list"),
            ("[1]", "is not an object"),
            ('"[{""name"": ""X""}]"', "is missing"),
        ],
    )
    def test_malformed_items(self, tmp_path, cell, fragment):
        row = GOOD_ROW.replace(
            '"[{""name"": ""X"", ""price"": 1.0, ""quantity"": 1, ""weight"": 0.0}]"', cell, 1
        )
        problems = validate_order_csv(write_csv(tmp_path, row))
        assert any("[items]" in p and fragment in p for p in problems)


class TestProblemsInTheJson:
    """The same for the customer file."""

    CASE = {
        "test_name": "x", "category": "valid_customers", "customer": {},
        "expected_valid": False, "expected_errors": ["something"], "reason": "r",
    }

    def test_test_cases_is_missing(self, tmp_path):
        problems = validate_customer_json(write_json(tmp_path, {"other": 1}))
        assert any("test_cases key is missing" in p for p in problems)

    def test_an_empty_list(self, tmp_path):
        problems = validate_customer_json(write_json(tmp_path, {"test_cases": []}))
        assert any("at least one case" in p for p in problems)

    def test_a_case_that_is_not_an_object(self, tmp_path):
        problems = validate_customer_json(write_json(tmp_path, {"test_cases": ["x"]}))
        assert any("is not an object" in p for p in problems)

    def test_a_case_with_missing_keys(self, tmp_path):
        problems = validate_customer_json(write_json(tmp_path, {"test_cases": [{"test_name": "x"}]}))
        assert any("is missing" in p for p in problems)

    def test_a_duplicated_name(self, tmp_path):
        problems = validate_customer_json(write_json(tmp_path, {"test_cases": [self.CASE, self.CASE]}))
        assert any("duplicated" in p for p in problems)

    def test_a_valid_case_listing_errors(self, tmp_path):
        case = {**self.CASE, "expected_valid": True, "expected_errors": ["something"]}
        problems = validate_customer_json(write_json(tmp_path, {"test_cases": [case]}))
        assert any("cannot list expected errors" in p for p in problems)

    def test_an_invalid_case_listing_no_errors(self, tmp_path):
        case = {**self.CASE, "expected_valid": False, "expected_errors": []}
        problems = validate_customer_json(write_json(tmp_path, {"test_cases": [case]}))
        assert any("must say which error it expects" in p for p in problems)

    def test_wrong_types(self, tmp_path):
        case = {**self.CASE, "expected_valid": "no", "expected_errors": "neither"}
        problems = validate_customer_json(write_json(tmp_path, {"test_cases": [case]}))
        assert any("must be a boolean" in p for p in problems)
        assert any("must be a list" in p for p in problems)


def test_require_valid_data_raises_with_everything_together(tmp_path):
    """The error gathers the problems from both files."""
    write_csv(tmp_path, GOOD_ROW.replace("ok,simple", "ok,invented", 1))
    write_json(tmp_path, {"test_cases": []})

    with pytest.raises(DataValidationError) as error:
        require_valid_data(str(tmp_path))

    assert "[category]" in str(error.value)
    assert "at least one case" in str(error.value)
