"""Field-level validation rules (pure functions) for customer data."""

import re
from datetime import date
from typing import Any, Optional, Tuple

US_STATES = frozenset(
    "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR "
    "PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split()
)
_EMAIL = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$"
)
_PHONE = re.compile(r"^\(\d{3}\) \d{3}-\d{4}$")
_ZIP = re.compile(r"^\d{5}(-\d{4})?$")
_EXPIRATION = re.compile(r"^(0[1-9]|1[0-2])/(\d{4})$")
_CVV = re.compile(r"^\d{3,4}$")


def is_valid_email(value: Any) -> bool:
    """Basic email format: local@domain.tld, no spaces and no consecutive dots."""
    return (
        isinstance(value, str) and ".." not in value and _EMAIL.match(value) is not None
    )


def is_valid_phone(value: Any) -> bool:
    """US phone in the form (XXX) XXX-XXXX."""
    return isinstance(value, str) and _PHONE.match(value) is not None


def is_non_empty_text(value: Any) -> bool:
    """Non-blank string (used for street and city)."""
    return isinstance(value, str) and value.strip() != ""


def is_valid_state(value: Any) -> bool:
    """Two-letter UPPERCASE US state (or DC) code."""
    return isinstance(value, str) and value in US_STATES


def is_valid_zip(value: Any) -> bool:
    """5-digit ZIP or ZIP+4 (12345-6789)."""
    return isinstance(value, str) and _ZIP.match(value) is not None


def luhn_check(number: str) -> bool:
    """Luhn checksum over a string of digits."""
    total = 0
    for position, char in enumerate(reversed(number)):
        digit = int(char)
        if position % 2 == 1:
            digit = digit * 2 - 9 if digit > 4 else digit * 2
        total += digit
    return total % 10 == 0


def is_valid_card_number(value: Any) -> bool:
    """13 to 19 digits only (no spaces or dashes) that pass the Luhn check."""
    if not isinstance(value, str) or not (value.isascii() and value.isdigit()):
        return False
    return 13 <= len(value) <= 19 and luhn_check(value)


def parse_expiration(value: Any) -> Optional[Tuple[int, int]]:
    """Parse "MM/YYYY" into (month, year); None when the format is wrong."""
    match = _EXPIRATION.match(value) if isinstance(value, str) else None
    return (int(match.group(1)), int(match.group(2))) if match else None


def is_expired(month: int, year: int, today: date) -> bool:
    """A card is valid through the last day of its expiration month."""
    return (year, month) < (today.year, today.month)


def is_valid_cvv(value: Any) -> bool:
    """3 or 4 digits."""
    return isinstance(value, str) and value.isascii() and _CVV.match(value) is not None
