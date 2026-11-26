"""Customer validator tests, driven by customer_validation.json.

Every case in the file carries the whole customer, whether it should be
valid, and the exact list of expected errors in the order validate_customer
produces them.
"""

import pytest

from conftest import load_json
from customer_validator import (
    ERRORS,
    is_valid_card_number,
    is_valid_email,
    is_valid_expiry,
    is_valid_phone,
    passes_luhn,
    validate_customer,
)

DATA = load_json("customer_validation.json")
CASES = DATA["test_cases"]
CATEGORY_MINIMUMS = {
    "valid_customers": 3,
    "invalid_emails": 4,
    "invalid_phones": 4,
    "invalid_addresses": 5,
    "invalid_cards": 8,
    "multiple_errors": 6,
}


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["test_name"])
def test_customer_validation(case):
    """The verdict and the full list of errors come from the file."""
    is_valid, errors = validate_customer(case["customer"])

    assert is_valid == case["expected_valid"], case["reason"]
    assert errors == case["expected_errors"], case["reason"]


class TestFileCoverage:
    """The file has to keep meeting what the brief asks for."""

    def test_minimum_number_of_cases(self):
        assert len(CASES) >= 30

    @pytest.mark.parametrize("category,minimum", sorted(CATEGORY_MINIMUMS.items()))
    def test_minimum_per_category(self, category, minimum):
        assert len([c for c in CASES if c["category"] == category]) >= minimum

    def test_every_rule_appears_failing_on_its_own(self):
        alone = {tuple(c["expected_errors"])[0] for c in CASES if len(c["expected_errors"]) == 1}
        assert alone == set(ERRORS.values())


class TestLuhn:
    """The algorithm on its own, without going through a whole customer."""

    @pytest.mark.parametrize(
        "number",
        ["4532015112830366", "4111111111111111", "5425233430109903", "378282246310005", "6011111111111117"],
    )
    def test_numbers_that_pass(self, number):
        assert passes_luhn(number) is True
        assert is_valid_card_number(number) is True

    @pytest.mark.parametrize("number", ["4532015112830367", "4111111111111112", "1234567890123"])
    def test_numbers_that_fail(self, number):
        assert is_valid_card_number(number) is False

    @pytest.mark.parametrize("number", ["4532 0151 1283 0366", "4532-0151-1283-0366"])
    def test_separators_are_ignored(self, number):
        assert is_valid_card_number(number) is True

    @pytest.mark.parametrize("length,valid", [(12, False), (13, True), (19, True), (20, False)])
    def test_length_boundaries(self, length, valid):
        """Builds a number of the requested length and fixes its check digit."""
        base = "4" + "0" * (length - 2)
        for last in "0123456789":
            if passes_luhn(base + last):
                assert is_valid_card_number(base + last) is valid
                return
        pytest.fail("no check digit found")

    @pytest.mark.parametrize("value", [None, 4532015112830366, [], {}])
    def test_values_that_are_not_text(self, value):
        assert is_valid_card_number(value) is False


class TestExpiry:
    """The reference date is November 2026, fixed in the module."""

    @pytest.mark.parametrize(
        "value,expected",
        [("11/26", True), ("12/26", True), ("10/26", False), ("01/27", True), ("12/25", False)],
    )
    def test_month_boundary(self, value, expected):
        assert is_valid_expiry(value) is expected

    @pytest.mark.parametrize("value", ["13/27", "00/27", "2027-12", "12/2027", "1227", "", None])
    def test_invalid_formats(self, value):
        assert is_valid_expiry(value) is False


class TestSingleFields:
    """Email and phone on their own."""

    @pytest.mark.parametrize(
        "value,expected",
        [("a@b.co", True), ("a@b", False), ("@b.co", False), ("a b@c.co", False), (None, False), (123, False)],
    )
    def test_email(self, value, expected):
        assert is_valid_email(value) is expected

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("(555) 123-4567", True),
            ("(555)123-4567", False),
            ("555-123-4567", False),
            (None, False),
            (5551234567, False),
        ],
    )
    def test_phone(self, value, expected):
        assert is_valid_phone(value) is expected

    def test_a_record_that_is_not_an_object_reports_everything(self):
        is_valid, errors = validate_customer("not a customer")
        assert is_valid is False
        assert errors == list(ERRORS.values())
