"""Validate contact, US billing and card details without retaining them."""

import re
from datetime import date

EMAIL = re.compile(
    r"[A-Za-z0-9_+%.-]+@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}"
)
PHONE = re.compile(r"\([0-9]{3}\) [0-9]{3}-[0-9]{4}")
ZIP = re.compile(r"[0-9]{5}(?:-[0-9]{4})?")
CARD_NUMBER = re.compile(r"[0-9]{13,19}")
EXPIRATION = re.compile(r"(0[1-9]|1[0-2])/([0-9]{4})")
CVV = re.compile(r"[0-9]{3,4}")
STATES = frozenset(
    (
        "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO "
        "MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC"
    ).split()
)


def _matches(pattern: re.Pattern[str], value: object) -> bool:
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def _has_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_email(value: object) -> bool:
    if not _matches(EMAIL, value):
        return False
    local_part = value.split("@", 1)[0]
    return not (
        local_part.startswith(".") or local_part.endswith(".") or ".." in local_part
    )


def _valid_card_number(number: object) -> bool:
    if not _matches(CARD_NUMBER, number) or not number.strip("0"):
        return False
    checksum = 0
    for index, digit in enumerate(reversed(number)):
        value = int(digit)
        if index % 2:
            value *= 2
            if value > 9:
                value -= 9
        checksum += value
    return checksum % 10 == 0


def _valid_expiration(expiration: object, today: date) -> bool:
    if not isinstance(expiration, str):
        return False
    match = EXPIRATION.fullmatch(expiration)
    if match is None:
        return False
    month, year = map(int, match.groups())
    # The card is valid through the last day of the printed month.
    return (year, month) >= (today.year, today.month)


def _address_errors(address: object) -> list[str]:
    if not isinstance(address, dict):
        return ["Invalid billing address"]
    errors = []
    for field in ("street", "city"):
        if not _has_text(address.get(field)):
            errors.append(f"Invalid billing {field}")
    state = address.get("state")
    if not isinstance(state, str) or state not in STATES:
        errors.append("Invalid billing state")
    if not _matches(ZIP, address.get("zip")):
        errors.append("Invalid billing ZIP code")
    return errors


def _card_errors(card: object, today: date) -> list[str]:
    if not isinstance(card, dict):
        return ["Invalid credit card"]
    errors = []
    if not _valid_card_number(card.get("number")):
        errors.append("Invalid credit card number")
    if not _valid_expiration(card.get("expiration"), today):
        errors.append("Invalid or expired credit card expiration date")
    if "cvv" in card and not _matches(CVV, card["cvv"]):
        errors.append("Invalid credit card CVV")
    return errors


def validate_customer(customer: object, *, today: date | None = None) -> dict:
    """Return validity and all field errors in a stable order."""
    if not isinstance(customer, dict):
        return {"is_valid": False, "errors": ["Invalid customer record"]}
    errors = []
    if not _valid_email(customer.get("email")):
        errors.append("Invalid email format")
    if not _matches(PHONE, customer.get("phone")):
        errors.append("Invalid phone format")
    errors.extend(_address_errors(customer.get("billing_address")))
    errors.extend(_card_errors(customer.get("credit_card"), today or date.today()))
    return {"is_valid": not errors, "errors": errors}
