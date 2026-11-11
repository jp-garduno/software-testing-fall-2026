"""Validate synthetic customer and payment details without external services."""

from datetime import date
import re

STATES = set(
    (
        "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV "
        "NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC"
    ).split()
)


def valid_card(number):
    """Accept ASCII digit card numbers of length 13–19 that pass Luhn."""
    if (
        not isinstance(number, str)
        or not re.fullmatch(r"[0-9]{13,19}", number)
        or set(number) == {"0"}
    ):
        return False
    digits = [int(char) for char in reversed(number)]
    checksum = sum(
        digit if index % 2 == 0 else (digit * 2 - 9 if digit > 4 else digit * 2)
        for index, digit in enumerate(digits)
    )
    return checksum % 10 == 0


def valid_expiration(expiration, today):
    """Cards remain valid through the last day of their expiration month."""
    if not isinstance(expiration, str) or not re.fullmatch(
        r"(0[1-9]|1[0-2])/[0-9]{4}", expiration
    ):
        return False
    month, year = map(int, expiration.split("/"))
    return (year, month) >= (today.year, today.month)


def validate_customer(customer, today=None):
    """Return a stable field-ordered error list; today can be injected in tests."""
    if not isinstance(customer, dict):
        return {"is_valid": False, "errors": ["Invalid customer"]}
    errors = []
    email = customer.get("email")
    if not isinstance(email, str) or not re.fullmatch(
        r"[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+", email
    ):
        errors.append("Invalid email format")
    phone = customer.get("phone")
    if not isinstance(phone, str) or not re.fullmatch(
        r"\([0-9]{3}\) [0-9]{3}-[0-9]{4}", phone
    ):
        errors.append("Invalid phone format")
    address = customer.get("billing_address")
    address = address if isinstance(address, dict) else {}
    for field in ("street", "city"):
        if not isinstance(address.get(field), str) or not address[field].strip():
            errors.append(f"Invalid billing {field}")
    state = address.get("state")
    if not isinstance(state, str) or state not in STATES:
        errors.append("Invalid billing state")
    zipcode = address.get("zip")
    if not isinstance(zipcode, str) or not re.fullmatch(
        r"[0-9]{5}(?:-[0-9]{4})?", zipcode
    ):
        errors.append("Invalid billing zip")
    card = customer.get("credit_card")
    card = card if isinstance(card, dict) else {}
    if not valid_card(card.get("number")):
        errors.append("Invalid credit card number")
    if not valid_expiration(card.get("expiration"), today or date.today()):
        errors.append("Invalid credit card expiration")
    cvv = card.get("cvv")
    if not isinstance(cvv, str) or not re.fullmatch(r"[0-9]{3,4}", cvv):
        errors.append("Invalid credit card CVV")
    return {"is_valid": not errors, "errors": errors}
