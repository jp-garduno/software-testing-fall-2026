"""Customer validation: email, phone, billing address and credit card.

``validate_customer`` checks every field and collects all the problems it
finds instead of stopping at the first one, so a form can show them together.
Errors always come out in the same order (email, phone, address, card) and use
the fixed messages below, which is what the JSON test data compares against.
"""

import re
from datetime import date
from typing import Dict, List, Optional

EMAIL_REQUIRED = "Email is required"
INVALID_EMAIL = "Invalid email format"
PHONE_REQUIRED = "Phone is required"
INVALID_PHONE = "Invalid phone format"
ADDRESS_REQUIRED = "Billing address is required"
STREET_REQUIRED = "Street is required"
CITY_REQUIRED = "City is required"
INVALID_CITY = "Invalid city"
INVALID_STATE = "Invalid state"
INVALID_ZIP = "Invalid ZIP code"
CARD_REQUIRED = "Credit card is required"
INVALID_CARD_NUMBER = "Invalid credit card number"
INVALID_EXPIRATION_FORMAT = "Invalid expiration date format"
CARD_EXPIRED = "Credit card is expired"
INVALID_CVV = "Invalid CVV"

# Local part: letters, digits and ._%+- without leading, trailing or doubled
# dots. Domain: dot-separated labels that do not start or end with a hyphen,
# ending in a TLD of at least two letters.
EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9_%+-]+(\.[A-Za-z0-9_%+-]+)*"
    r"@([A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}$"
)
# US format (XXX) XXX-XXXX. NANP area codes never start with 0 or 1.
PHONE_PATTERN = re.compile(r"^\([2-9]\d{2}\) \d{3}-\d{4}$")
CITY_PATTERN = re.compile(r"^[A-Za-z]+([ .'-]+[A-Za-z]+)*\.?$")
ZIP_PATTERN = re.compile(r"^\d{5}(-\d{4})?$")
EXPIRATION_PATTERN = re.compile(r"^(0[1-9]|1[0-2])/(\d{4})$")
CARD_SEPARATORS = re.compile(r"[ -]")

US_STATES = frozenset(
    "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ "
    "NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split()
)


def _is_blank(value) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def is_valid_email(email: str) -> bool:
    """True if the email looks like local@domain.tld (max 254 characters)."""
    return isinstance(email, str) and len(email) <= 254 and EMAIL_PATTERN.match(email) is not None


def is_valid_phone(phone: str) -> bool:
    """True if the phone follows the US format (XXX) XXX-XXXX."""
    return isinstance(phone, str) and PHONE_PATTERN.match(phone) is not None


def luhn_check(number: str) -> bool:
    """True if a string of digits passes the Luhn checksum."""
    if not number.isdigit():
        return False
    total = 0
    # Double every second digit from the right; subtracting 9 equals adding its digits.
    for position, char in enumerate(reversed(number)):
        digit = int(char)
        if position % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def normalize_card_number(number) -> str:
    """Remove the spaces and dashes people type between digit groups."""
    return CARD_SEPARATORS.sub("", number) if isinstance(number, str) else ""


def is_valid_card_number(number: str) -> bool:
    """True for 13 to 19 digits (separators allowed) that pass the Luhn check."""
    digits = normalize_card_number(number)
    return 13 <= len(digits) <= 19 and luhn_check(digits)


def validate_address(address) -> List[str]:
    """Return the errors found in a billing address dict."""
    if not isinstance(address, dict):
        return [ADDRESS_REQUIRED]
    errors = []
    if _is_blank(address.get("street")):
        errors.append(STREET_REQUIRED)
    city = address.get("city")
    if _is_blank(city):
        errors.append(CITY_REQUIRED)
    elif not isinstance(city, str) or not CITY_PATTERN.match(city.strip()):
        errors.append(INVALID_CITY)
    if address.get("state") not in US_STATES:
        errors.append(INVALID_STATE)
    zip_code = address.get("zip")
    if not isinstance(zip_code, str) or not ZIP_PATTERN.match(zip_code):
        errors.append(INVALID_ZIP)
    return errors


def _expiration_errors(expiration, today: date) -> List[str]:
    match = EXPIRATION_PATTERN.match(expiration) if isinstance(expiration, str) else None
    if match is None:
        return [INVALID_EXPIRATION_FORMAT]
    month, year = int(match.group(1)), int(match.group(2))
    # A card is good through the last day of its expiration month.
    if (year, month) < (today.year, today.month):
        return [CARD_EXPIRED]
    return []


def validate_credit_card(card, today: Optional[date] = None) -> List[str]:
    """Return the errors found in a credit card dict (number, expiration, cvv)."""
    if not isinstance(card, dict):
        return [CARD_REQUIRED]
    errors = []
    digits = normalize_card_number(card.get("number"))
    if not is_valid_card_number(card.get("number")):
        errors.append(INVALID_CARD_NUMBER)
    errors.extend(_expiration_errors(card.get("expiration"), today or date.today()))
    # American Express (34, 37) prints a four-digit code; every other network uses three.
    cvv_length = 4 if digits[:2] in ("34", "37") else 3
    cvv = card.get("cvv")
    if not isinstance(cvv, str) or not cvv.isdigit() or len(cvv) != cvv_length:
        errors.append(INVALID_CVV)
    return errors


def validate_customer(customer: Dict, today: Optional[date] = None) -> Dict:
    """
    Validate every customer field.

    Args:
        customer: {"email", "phone", "billing_address": {...}, "credit_card": {...}}
        today: Date used for the expiration check, today by default.

    Returns:
        {"is_valid": bool, "errors": [str, ...]}
    """
    errors = []
    email = customer.get("email")
    if _is_blank(email):
        errors.append(EMAIL_REQUIRED)
    elif not is_valid_email(email):
        errors.append(INVALID_EMAIL)

    phone = customer.get("phone")
    if _is_blank(phone):
        errors.append(PHONE_REQUIRED)
    elif not is_valid_phone(phone):
        errors.append(INVALID_PHONE)

    errors.extend(validate_address(customer.get("billing_address")))
    errors.extend(validate_credit_card(customer.get("credit_card"), today))
    return {"is_valid": not errors, "errors": errors}
