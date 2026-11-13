"""Customer validation: email, phone, billing address and credit card details."""

import re
from datetime import date
from typing import Dict, List, Optional

ERR_EMAIL = "Invalid email format"
ERR_PHONE = "Invalid phone format"
ERR_STREET = "Invalid street"
ERR_CITY = "Invalid city"
ERR_STATE = "Invalid state"
ERR_ZIP = "Invalid zip code"
ERR_CARD_NUMBER = "Invalid credit card number"
ERR_EXPIRATION = "Invalid expiration date"
ERR_EXPIRED = "Credit card expired"
ERR_CVV = "Invalid CVV"

_LOCAL = r"[A-Za-z0-9_%+-]+(\.[A-Za-z0-9_%+-]+)*"
_LABEL = r"[A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?"
EMAIL_RE = re.compile(rf"^{_LOCAL}@{_LABEL}(\.{_LABEL})*\.[A-Za-z]{{2,}}$")
PHONE_RE = re.compile(r"^\(\d{3}\) \d{3}-\d{4}$")
ZIP_RE = re.compile(r"^\d{5}(-\d{4})?$")
CITY_RE = re.compile(r"^[A-Za-z][A-Za-z .'-]{1,49}$")
EXPIRATION_RE = re.compile(r"^(0[1-9]|1[0-2])/(\d{4})$")

US_STATES = frozenset(
    "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA "
    "RI SC SD TN TX UT VT VA WA WV WI WY DC".split()
)
MAX_EMAIL_LENGTH = 254
MAX_STREET_LENGTH = 100


def _text(value):
    """Return value as a string, treating anything that is not a string as empty."""
    return value if isinstance(value, str) else ""


def luhn_is_valid(digits: str) -> bool:
    """Return True if a string of digits passes the Luhn checksum."""
    if not digits.isdigit():
        return False
    total = 0
    for position, char in enumerate(reversed(digits)):
        digit = int(char)
        if position % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def normalize_card_number(number) -> str:
    """Strip spaces and hyphens from a card number; non-strings become an empty string."""
    return re.sub(r"[ -]", "", number) if isinstance(number, str) else ""


def is_valid_email(email) -> bool:
    """Check basic email syntax and length."""
    email = _text(email)
    return len(email) <= MAX_EMAIL_LENGTH and EMAIL_RE.match(email) is not None


def is_valid_phone(phone) -> bool:
    """Check the US format (XXX) XXX-XXXX."""
    return PHONE_RE.match(_text(phone)) is not None


def is_valid_street(street) -> bool:
    """A street needs at least one letter and one digit and at most 100 characters."""
    street = _text(street).strip()
    return (
        0 < len(street) <= MAX_STREET_LENGTH
        and any(char.isdigit() for char in street)
        and any(char.isalpha() for char in street)
    )


def is_valid_card_number(number) -> bool:
    """13-19 digits (spaces and hyphens allowed) that pass the Luhn check."""
    digits = normalize_card_number(number)
    return 13 <= len(digits) <= 19 and luhn_is_valid(digits)


def is_valid_cvv(cvv, card_number) -> bool:
    """CVV is 4 digits for American Express (34/37 prefix) and 3 digits for other cards."""
    expected_length = 4 if normalize_card_number(card_number)[:2] in ("34", "37") else 3
    cvv = _text(cvv)
    return cvv.isascii() and cvv.isdigit() and len(cvv) == expected_length


def validate_expiration(expiration, today: date) -> Optional[str]:
    """Return an error message for a bad or past MM/YYYY expiration, else None.

    A card is valid through the last day of its expiration month.
    """
    match = EXPIRATION_RE.match(_text(expiration))
    if match is None:
        return ERR_EXPIRATION
    month, year = int(match.group(1)), int(match.group(2))
    if (year, month) < (today.year, today.month):
        return ERR_EXPIRED
    return None


def validate_customer(customer: Dict, today: Optional[date] = None) -> Dict:
    """Validate a customer record.

    Returns {"is_valid": bool, "errors": [str, ...]}. Errors appear in a fixed order: email, phone,
    street, city, state, zip, card number, expiration, CVV. Missing fields count as invalid.
    """
    today = today or date.today()
    address = customer.get("billing_address") or {}
    card = customer.get("credit_card") or {}
    errors: List[str] = []

    checks = (
        (ERR_EMAIL, is_valid_email(customer.get("email"))),
        (ERR_PHONE, is_valid_phone(customer.get("phone"))),
        (ERR_STREET, is_valid_street(address.get("street"))),
        (ERR_CITY, CITY_RE.match(_text(address.get("city")).strip()) is not None),
        (ERR_STATE, _text(address.get("state")) in US_STATES),
        (ERR_ZIP, ZIP_RE.match(_text(address.get("zip"))) is not None),
        (ERR_CARD_NUMBER, is_valid_card_number(card.get("number"))),
    )
    errors.extend(message for message, ok in checks if not ok)

    expiration_error = validate_expiration(card.get("expiration"), today)
    if expiration_error:
        errors.append(expiration_error)
    if not is_valid_cvv(card.get("cvv"), card.get("number")):
        errors.append(ERR_CVV)

    return {"is_valid": not errors, "errors": errors}
