"""Validate customer contact, billing and payment information."""

import re
from collections.abc import Mapping
from datetime import date

EMAIL = re.compile(
    r"[A-Za-z0-9_%+~-]+(?:\.[A-Za-z0-9_%+~-]+)*"
    r"@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}"
)
PHONE = re.compile(r"\([0-9]{3}\) [0-9]{3}-[0-9]{4}")
ZIP = re.compile(r"[0-9]{5}(?:-[0-9]{4})?")
CARD_NUMBER = re.compile(r"[0-9]{13,19}")
EXPIRATION = re.compile(r"(0[1-9]|1[0-2])/([0-9]{4})")
CVV = re.compile(r"[0-9]{3,4}")
STATES = frozenset(
    "AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO "
    "MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split()
)


def _matches(pattern, value):
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def _present(value):
    return isinstance(value, str) and bool(value.strip())


def _valid_card(number):
    if not _matches(CARD_NUMBER, number) or set(number) == {"0"}:
        return False
    checksum = 0
    for index, digit in enumerate(reversed(number)):
        value = int(digit) * (2 if index % 2 else 1)
        checksum += value if value < 10 else value - 9
    return checksum % 10 == 0


def _valid_expiration(expiration, today):
    match = EXPIRATION.fullmatch(expiration) if isinstance(expiration, str) else None
    if match is None:
        return False
    month, year = map(int, match.groups())
    return (year, month) >= (today.year, today.month)


def _address_errors(address):
    if not isinstance(address, Mapping):
        return ["Missing billing address"]
    checks = (
        (_present(address.get("street")), "Missing billing street"),
        (_present(address.get("city")), "Missing billing city"),
        (
            isinstance(address.get("state"), str) and address["state"] in STATES,
            "Invalid billing state",
        ),
        (_matches(ZIP, address.get("zip")), "Invalid billing ZIP code"),
    )
    return [message for valid, message in checks if not valid]


def _card_errors(card, today):
    if not isinstance(card, Mapping):
        return ["Missing credit card"]
    checks = (
        (_valid_card(card.get("number")), "Invalid credit card number"),
        (
            _valid_expiration(card.get("expiration"), today),
            "Invalid credit card expiration",
        ),
        (_matches(CVV, card.get("cvv")), "Invalid credit card CVV"),
    )
    return [message for valid, message in checks if not valid]


def validate_customer(customer, *, today=None):
    """Return validity and all applicable errors in field order."""
    if not isinstance(customer, Mapping):
        return {"is_valid": False, "errors": ["Invalid customer data"]}
    errors = []
    if not _matches(EMAIL, customer.get("email")):
        errors.append("Invalid email format")
    if not _matches(PHONE, customer.get("phone")):
        errors.append("Invalid phone format")
    errors.extend(_address_errors(customer.get("billing_address")))
    errors.extend(_card_errors(customer.get("credit_card"), today or date.today()))
    return {"is_valid": not errors, "errors": errors}
