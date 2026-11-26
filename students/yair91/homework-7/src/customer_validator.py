"""Customer validation for the order processing system.

Every check returns its own message, and validate_customer collects all of
them instead of stopping at the first, so a form can show everything that is
wrong in one pass.
"""

import re
from typing import List, Tuple

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}$")
PHONE_PATTERN = re.compile(r"^\(\d{3}\) \d{3}-\d{4}$")
ZIP_PATTERN = re.compile(r"^\d{5}(-\d{4})?$")
STATE_PATTERN = re.compile(r"^[A-Z]{2}$")
EXPIRY_PATTERN = re.compile(r"^(0[1-9]|1[0-2])/\d{2}$")

CARD_MIN_DIGITS = 13
CARD_MAX_DIGITS = 19
STREET_MIN_LENGTH = 5
CITY_MIN_LENGTH = 2

ERRORS = {
    "email": "Invalid email format",
    "phone": "Phone must match (XXX) XXX-XXXX",
    "street": f"Street must be at least {STREET_MIN_LENGTH} characters",
    "city": f"City must be at least {CITY_MIN_LENGTH} characters",
    "state": "State must be a 2-letter uppercase code",
    "zip": "Zip must be 5 digits or ZIP+4",
    "card_number": "Credit card number failed validation",
    "card_expiry": "Card expiry must be MM/YY and not in the past",
}

# Reference "today" for expiry checks. Kept as data rather than datetime.now()
# so the test data stays correct no matter when the suite runs.
REFERENCE_YEAR = 2026
REFERENCE_MONTH = 11


def is_valid_email(email) -> bool:
    """Accept a well-formed address with a non-empty label in every position."""
    if not isinstance(email, str) or not email or " " in email:
        return False
    return bool(EMAIL_PATTERN.match(email))


def is_valid_phone(phone) -> bool:
    """Accept only the US format the brief asks for: (XXX) XXX-XXXX."""
    return isinstance(phone, str) and bool(PHONE_PATTERN.match(phone))


def passes_luhn(digits: str) -> bool:
    """Run the Luhn checksum over a string of digits."""
    total = 0
    for position, char in enumerate(reversed(digits)):
        value = int(char)
        if position % 2 == 1:
            value *= 2
            if value > 9:
                value -= 9
        total += value
    return total % 10 == 0


def is_valid_card_number(number) -> bool:
    """Accept 13 to 19 digits, spaces or dashes allowed, that pass Luhn."""
    if not isinstance(number, str):
        return False

    digits = number.replace(" ", "").replace("-", "")
    if not digits.isdigit() or not CARD_MIN_DIGITS <= len(digits) <= CARD_MAX_DIGITS:
        return False
    return passes_luhn(digits)


def is_valid_expiry(expiry, year: int = REFERENCE_YEAR, month: int = REFERENCE_MONTH) -> bool:
    """Accept MM/YY in the two-digit 2000s, from the reference month onward."""
    if not isinstance(expiry, str) or not EXPIRY_PATTERN.match(expiry):
        return False

    card_month, card_year = (int(part) for part in expiry.split("/"))
    return (2000 + card_year, card_month) >= (year, month)


def validate_address(address) -> List[str]:
    """Return every problem found in the billing address."""
    if not isinstance(address, dict):
        return [ERRORS["street"], ERRORS["city"], ERRORS["state"], ERRORS["zip"]]

    errors = []
    street = address.get("street")
    if not isinstance(street, str) or len(street.strip()) < STREET_MIN_LENGTH:
        errors.append(ERRORS["street"])

    city = address.get("city")
    if not isinstance(city, str) or len(city.strip()) < CITY_MIN_LENGTH:
        errors.append(ERRORS["city"])

    state = address.get("state")
    if not isinstance(state, str) or not STATE_PATTERN.match(state):
        errors.append(ERRORS["state"])

    zip_code = address.get("zip")
    if not isinstance(zip_code, str) or not ZIP_PATTERN.match(zip_code):
        errors.append(ERRORS["zip"])

    return errors


def validate_customer(customer) -> Tuple[bool, List[str]]:
    """Validate a whole customer record.

    Returns (is_valid, errors) with every problem found, in a fixed order so
    the data files can list the expected errors deterministically.
    """
    if not isinstance(customer, dict):
        return (False, list(ERRORS.values()))

    errors = []
    if not is_valid_email(customer.get("email")):
        errors.append(ERRORS["email"])
    if not is_valid_phone(customer.get("phone")):
        errors.append(ERRORS["phone"])

    errors.extend(validate_address(customer.get("address")))

    if not is_valid_card_number(customer.get("card_number")):
        errors.append(ERRORS["card_number"])
    if not is_valid_expiry(customer.get("card_expiry")):
        errors.append(ERRORS["card_expiry"])

    return (len(errors) == 0, errors)
