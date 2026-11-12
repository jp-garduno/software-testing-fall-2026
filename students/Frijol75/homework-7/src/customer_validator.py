"""
Customer Validator Module - E-Commerce Order Processing System.

Validates customer profile data:
    - Email format
    - US phone number format: (XXX) XXX-XXXX
    - Billing address (street, city, valid US state, 5 or 5+4 zip code)
    - Credit card (13-19 digits Luhn algorithm, MM/YYYY expiration, 3-4 digit CVV)
"""

import re
from datetime import date
from typing import Dict, List, Optional

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")
PHONE_REGEX = re.compile(r"^\(\d{3}\) \d{3}-\d{4}$")
ZIP_REGEX = re.compile(r"^\d{5}(-\d{4})?$")
EXPIRATION_REGEX = re.compile(r"^(0[1-9]|1[0-2])/(\d{4})$")
CVV_REGEX = re.compile(r"^\d{3,4}$")

US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC",
}


def validate_email(email: Optional[str]) -> List[str]:
    """Validate email format."""
    if not email:
        return ["Missing email"]
    if ".." in email or not EMAIL_REGEX.match(email):
        return ["Invalid email format"]
    return []


def validate_phone(phone: Optional[str]) -> List[str]:
    """Validate phone format (US standard: (XXX) XXX-XXXX)."""
    if not phone:
        return ["Missing phone"]
    if not PHONE_REGEX.match(phone):
        return ["Invalid phone format"]
    return []


def validate_address(address: Optional[Dict]) -> List[str]:
    """Validate billing address fields (street, city, state, zip)."""
    if not address or not isinstance(address, dict):
        return ["Missing billing address"]

    errors = []
    if not str(address.get("street", "")).strip():
        errors.append("Missing street")
    if not str(address.get("city", "")).strip():
        errors.append("Missing city")
    if address.get("state") not in US_STATES:
        errors.append("Invalid state")
    if not ZIP_REGEX.match(str(address.get("zip", "")).strip()):
        errors.append("Invalid zip code")
    return errors


def luhn_check(number: str) -> bool:
    """
    Validate credit card number using the Luhn checksum algorithm.
    """
    if not number.isdigit():
        return False
    total = 0
    for i, ch in enumerate(reversed(number)):
        digit = int(ch)
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def validate_expiration(expiration: Optional[str], today: Optional[date] = None) -> List[str]:
    """Validate expiration format MM/YYYY and ensure card is not expired."""
    ref_date = today or date.today()
    if not expiration:
        return ["Invalid expiration format"]

    match = EXPIRATION_REGEX.match(str(expiration).strip())
    if not match:
        return ["Invalid expiration format"]

    month = int(match.group(1))
    year = int(match.group(2))

    if (year, month) < (ref_date.year, ref_date.month):
        return ["Credit card expired"]
    return []


def validate_credit_card(card: Optional[Dict], today: Optional[date] = None) -> List[str]:
    """Validate credit card number (Luhn), expiration, and CVV."""
    if not card or not isinstance(card, dict):
        return ["Missing credit card"]

    errors = []
    raw_number = str(card.get("number", "")).replace(" ", "").replace("-", "")
    if not (13 <= len(raw_number) <= 19) or not luhn_check(raw_number):
        errors.append("Invalid credit card number")

    errors.extend(validate_expiration(card.get("expiration"), today))

    if not CVV_REGEX.match(str(card.get("cvv", "")).strip()):
        errors.append("Invalid CVV")

    return errors


def validate_customer(customer: Dict, today: Optional[date] = None) -> Dict:
    """
    Validate customer registration / order placement details.

    Args:
        customer: Dict with email, phone, billing_address, and credit_card.
        today: Reference date for card expiration.

    Returns:
        {"is_valid": bool, "errors": List[str]}
    """
    if not customer or not isinstance(customer, dict):
        return {
            "is_valid": False,
            "errors": ["Invalid customer payload"],
        }

    errors = []
    errors.extend(validate_email(customer.get("email")))
    errors.extend(validate_phone(customer.get("phone")))
    errors.extend(validate_address(customer.get("billing_address")))
    errors.extend(validate_credit_card(customer.get("credit_card"), today))

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
    }

