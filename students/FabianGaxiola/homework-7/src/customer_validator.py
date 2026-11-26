"""Validation rules for customer details used by the order system."""

import re
from datetime import date
from typing import Any, Mapping

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN = re.compile(r"^\(\d{3}\) \d{3}-\d{4}$")
ZIP_PATTERN = re.compile(r"^\d{5}(?:-\d{4})?$")
EXPIRATION_PATTERN = re.compile(r"^(\d{2})/(\d{4})$")


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _luhn_is_valid(number: str) -> bool:
    digits = number.replace(" ", "").replace("-", "")
    if not digits.isdigit() or not 13 <= len(digits) <= 19:
        return False
    checksum = 0
    parity = len(digits) % 2
    for index, character in enumerate(digits):
        digit = int(character)
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def _valid_expiration(value: Any, today: date) -> bool:
    if not isinstance(value, str):
        return False
    match = EXPIRATION_PATTERN.fullmatch(value)
    if match is None:
        return False
    month, year = (int(part) for part in match.groups())
    return 1 <= month <= 12 and (year, month) >= (today.year, today.month)


def _validate_address(value: Any) -> list[str]:
    if not isinstance(value, Mapping):
        return ["Invalid billing address"]

    address = _mapping(value)
    errors = []
    for field in ("street", "city"):
        field_value = address.get(field)
        if not isinstance(field_value, str) or not field_value.strip():
            errors.append(f"Invalid billing address: {field} is required")
    state = address.get("state")
    if not isinstance(state, str) or re.fullmatch(r"[A-Z]{2}", state) is None:
        errors.append("Invalid billing address: state must be a two-letter code")
    zip_code = address.get("zip")
    if not isinstance(zip_code, str) or ZIP_PATTERN.fullmatch(zip_code) is None:
        errors.append("Invalid billing address: ZIP code is invalid")
    return errors


def _validate_credit_card(value: Any, today: date) -> list[str]:
    if not isinstance(value, Mapping):
        return ["Invalid credit card"]

    card = _mapping(value)
    errors = []
    number = card.get("number")
    if not isinstance(number, str) or not _luhn_is_valid(number):
        errors.append("Invalid credit card number")
    if not _valid_expiration(card.get("expiration"), today):
        errors.append("Invalid credit card expiration")
    cvv = card.get("cvv")
    if not isinstance(cvv, str) or re.fullmatch(r"\d{3,4}", cvv) is None:
        errors.append("Invalid credit card CVV")
    return errors


def validate_customer(customer: Any, today: date | None = None) -> dict[str, Any]:
    """Return whether a customer is valid and an ordered list of validation errors."""
    current_date = today if today is not None else date.today()
    customer_data = _mapping(customer)
    errors: list[str] = []

    email = customer_data.get("email")
    if not isinstance(email, str) or EMAIL_PATTERN.fullmatch(email) is None:
        errors.append("Invalid email format")

    phone = customer_data.get("phone")
    if not isinstance(phone, str) or PHONE_PATTERN.fullmatch(phone) is None:
        errors.append("Invalid phone format")

    errors.extend(_validate_address(customer_data.get("billing_address")))
    errors.extend(_validate_credit_card(customer_data.get("credit_card"), current_date))

    return {"is_valid": not errors, "errors": errors}
