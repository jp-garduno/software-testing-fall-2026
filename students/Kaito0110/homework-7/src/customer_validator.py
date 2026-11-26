"""Customer validator module for e-commerce checkout and payment validation."""

import re
from typing import Any, Dict, List, Tuple

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)
PHONE_PATTERN = re.compile(r"^\(\d{3}\) \d{3}-\d{4}$")
ZIP_PATTERN = re.compile(r"^\d{5}(-\d{4})?$")
STATE_PATTERN = re.compile(r"^[A-Z]{2}$")
EXPIRATION_PATTERN = re.compile(r"^(0[1-9]|1[0-2])/(\d{4})$")
CVV_PATTERN = re.compile(r"^\d{3,4}$")


def validate_email(email: Any) -> bool:
    """Validate email format."""
    if not isinstance(email, str) or not email.strip():
        return False
    if ".." in email:
        return False
    return bool(EMAIL_PATTERN.match(email.strip()))


def validate_phone(phone: Any) -> bool:
    """Validate US phone format: (XXX) XXX-XXXX."""
    if not isinstance(phone, str):
        return False
    return bool(PHONE_PATTERN.match(phone))


def validate_billing_address(address: Any) -> Tuple[bool, List[str]]:
    """Validate billing address dictionary (street, city, state, zip)."""
    errors: List[str] = []
    if not isinstance(address, dict):
        return False, ["Invalid billing address"]

    street = address.get("street", "")
    city = address.get("city", "")
    state = address.get("state", "")
    zip_code = address.get("zip", "")

    if not isinstance(street, str) or not street.strip():
        errors.append("Invalid street address")
    if not isinstance(city, str) or not city.strip():
        errors.append("Invalid city")
    if not isinstance(state, str) or not STATE_PATTERN.match(state.strip()):
        errors.append("Invalid state code")
    if not isinstance(zip_code, str) or not ZIP_PATTERN.match(zip_code.strip()):
        errors.append("Invalid zip code")

    return len(errors) == 0, errors


def check_luhn(card_number: str) -> bool:
    """Verify credit card number using the Luhn checksum algorithm."""
    digits = [int(ch) for ch in card_number]
    checksum = 0
    parity = len(digits) % 2
    for idx, digit in enumerate(digits):
        if idx % 2 == parity:
            doubled = digit * 2
            checksum += doubled - 9 if doubled > 9 else doubled
        else:
            checksum += digit
    return checksum % 10 == 0


def validate_credit_card(
    credit_card: Any, reference_year: int = 2025, reference_month: int = 1
) -> Tuple[bool, List[str]]:
    """Validate credit card number (Luhn), expiration date, and CVV."""
    errors: List[str] = []
    if not isinstance(credit_card, dict):
        return False, ["Invalid credit card information"]

    number = str(credit_card.get("number", "")).replace(" ", "").replace("-", "")
    expiration = str(credit_card.get("expiration", ""))
    cvv = str(credit_card.get("cvv", ""))

    if not number.isdigit() or not 13 <= len(number) <= 19 or not check_luhn(number):
        errors.append("Invalid credit card number")

    exp_match = EXPIRATION_PATTERN.match(expiration)
    if not exp_match:
        errors.append("Invalid credit card expiration date")
    else:
        exp_month = int(exp_match.group(1))
        exp_year = int(exp_match.group(2))
        if (exp_year, exp_month) < (reference_year, reference_month):
            errors.append("Credit card expired")

    if not CVV_PATTERN.match(cvv):
        errors.append("Invalid CVV")

    return len(errors) == 0, errors


def validate_customer(
    customer: Dict[str, Any],
    reference_year: int = 2025,
    reference_month: int = 1,
) -> Dict[str, Any]:
    """
    Validate all customer fields and return validation status and errors.

    Returns:
        {"is_valid": bool, "errors": List[str]}
    """
    if not isinstance(customer, dict):
        return {"is_valid": False, "errors": ["Invalid customer payload"]}

    errors: List[str] = []

    if not validate_email(customer.get("email")):
        errors.append("Invalid email format")

    if not validate_phone(customer.get("phone")):
        errors.append("Invalid phone format")

    _, address_errors = validate_billing_address(customer.get("billing_address"))
    errors.extend(address_errors)

    _, card_errors = validate_credit_card(
        customer.get("credit_card"),
        reference_year=reference_year,
        reference_month=reference_month,
    )
    errors.extend(card_errors)

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
    }
