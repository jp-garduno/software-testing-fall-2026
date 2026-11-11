"""Customer validation for checkout: contact data, billing address and credit card.

The checks are declared as a table (FIELD_RULES): where the value lives in the
customer record, the function that accepts or rejects it, and the message to
report. validate_customer walks that table, so a new rule is a new row.
"""

import re
from datetime import date
from typing import Any, Dict, Optional

EMAIL = re.compile(r"[^@\s]+@[^@\s.]+(\.[^@\s.]+)+")
PHONE = re.compile(r"\(\d{3}\) \d{3}-\d{4}")
ZIP_CODE = re.compile(r"\d{5}(-\d{4})?")
CARD_NUMBER = re.compile(r"\d{13,19}")
CVV = re.compile(r"\d{3,4}")
EXPIRATION = re.compile(r"(0[1-9]|1[0-2])/\d{4}")

# The 50 states plus the District of Columbia.
US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL",
    "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT",
    "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
    "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC",
}


def _matches(pattern: "re.Pattern[str]", value: Any) -> bool:
    """True when value is a string that matches the whole pattern.

    Missing values (None) and numbers never match, so callers need no type checks.
    """
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def is_valid_email(email: Any) -> bool:
    """Accept name@domain.tld: one @, no spaces, at least one dot after the @."""
    return _matches(EMAIL, email)


def is_valid_phone(phone: Any) -> bool:
    """Accept the US format (XXX) XXX-XXXX and nothing else."""
    return _matches(PHONE, phone)


def is_filled(text: Any) -> bool:
    """Accept any string that is more than blank space."""
    return isinstance(text, str) and bool(text.strip())


def is_valid_state(state: Any) -> bool:
    """Accept the two-letter, upper-case code of a US state."""
    return isinstance(state, str) and state in US_STATES


def is_valid_zip(zip_code: Any) -> bool:
    """Accept five digits, optionally followed by -XXXX (ZIP+4)."""
    return _matches(ZIP_CODE, zip_code)


def is_valid_cvv(cvv: Any) -> bool:
    """Accept three or four digits."""
    return _matches(CVV, cvv)


def passes_luhn(number: Any) -> bool:
    """Accept 13 to 19 digits whose Luhn checksum ends in zero.

    From the right, every second digit is doubled and its two digits are added
    (14 counts as 1 + 4); the sum of everything must be a multiple of 10.
    """
    if not _matches(CARD_NUMBER, number):
        return False

    digits = [int(char) for char in reversed(number)]
    doubled = (sum(divmod(2 * digit, 10)) for digit in digits[1::2])
    return (sum(digits[0::2]) + sum(doubled)) % 10 == 0


def expiration_error(expiration: Any, today: date) -> Optional[str]:
    """Return why a card expiration (MM/YYYY) cannot be used on `today`, or None.

    A card stays valid through the last day of its expiration month.
    """
    if not _matches(EXPIRATION, expiration):
        return "Invalid expiration date"

    month, year = (int(part) for part in expiration.split("/"))
    if (year, month) < (today.year, today.month):
        return "Credit card expired"
    return None


# (path inside the customer record, check, message when the check fails)
FIELD_RULES = (
    ("email", is_valid_email, "Invalid email format"),
    ("phone", is_valid_phone, "Invalid phone format"),
    ("billing_address.street", is_filled, "Missing street"),
    ("billing_address.city", is_filled, "Missing city"),
    ("billing_address.state", is_valid_state, "Invalid state"),
    ("billing_address.zip", is_valid_zip, "Invalid zip code"),
    ("credit_card.number", passes_luhn, "Invalid credit card number"),
    ("credit_card.cvv", is_valid_cvv, "Invalid CVV"),
)


def _lookup(record: Any, path: str) -> Any:
    """Follow a dotted path through nested dicts; None once a level is missing."""
    for key in path.split("."):
        record = record.get(key) if isinstance(record, dict) else None
    return record


def validate_customer(customer: Dict[str, Any], today: Optional[date] = None) -> Dict[str, Any]:
    """Validate a customer record.

    Args:
        customer: {"email", "phone", "billing_address": {...}, "credit_card": {...}}
        today: date used to decide whether the card has expired; defaults to the
            real date. Tests pass a fixed date so results never change with time.

    Returns:
        {"is_valid": bool, "errors": [str]} with the errors in FIELD_RULES order
        and the expiration error, if any, last.
    """
    errors = [message for path, is_ok, message in FIELD_RULES if not is_ok(_lookup(customer, path))]

    expiration = _lookup(customer, "credit_card.expiration")
    expiration_problem = expiration_error(expiration, today or date.today())
    if expiration_problem:
        errors.append(expiration_problem)

    return {"is_valid": not errors, "errors": errors}
