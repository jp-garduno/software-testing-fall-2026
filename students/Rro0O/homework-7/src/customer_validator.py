"""Customer validation: email, phone, billing address and credit card."""

import re
from datetime import date
from typing import Dict, List, Optional

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")
PHONE_RE = re.compile(r"^\(\d{3}\) \d{3}-\d{4}$")
ZIP_RE = re.compile(r"^\d{5}(-\d{4})?$")
EXPIRATION_RE = re.compile(r"^(0[1-9]|1[0-2])/(\d{4})$")
CVV_RE = re.compile(r"^\d{3,4}$")

US_STATES = frozenset(
    "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS "
    "MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV "
    "WI WY DC".split()
)

ERR_EMAIL = "Invalid email format"
ERR_PHONE = "Invalid phone format"
ERR_NO_ADDRESS = "Missing billing address"
ERR_STREET = "Invalid street"
ERR_CITY = "Invalid city"
ERR_STATE = "Invalid state"
ERR_ZIP = "Invalid zip code"
ERR_NO_CARD = "Missing credit card"
ERR_CARD_NUMBER = "Invalid credit card number"
ERR_EXP_FORMAT = "Invalid expiration format"
ERR_EXPIRED = "Credit card expired"
ERR_CVV = "Invalid CVV"


def _text(value) -> str:
    return value.strip() if isinstance(value, str) else ""


def validate_email(email) -> bool:
    """True when the email looks like local@domain.tld."""
    return isinstance(email, str) and bool(EMAIL_RE.match(email)) and ".." not in email


def validate_phone(phone) -> bool:
    """True for the US format (XXX) XXX-XXXX."""
    return isinstance(phone, str) and bool(PHONE_RE.match(phone))


def luhn_check(number) -> bool:
    """Luhn checksum over a 13-19 digit string."""
    if not isinstance(number, str) or not number.isdigit():
        return False
    if not 13 <= len(number) <= 19:
        return False
    total = 0
    for index, char in enumerate(reversed(number)):
        digit = int(char)
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def validate_expiration(expiration, today: Optional[date] = None) -> Optional[str]:
    """Return None if valid, otherwise an error message.

    The card is valid through the last day of its expiration month.
    """
    today = today or date.today()
    match = EXPIRATION_RE.match(expiration) if isinstance(expiration, str) else None
    if not match:
        return ERR_EXP_FORMAT
    month, year = int(match.group(1)), int(match.group(2))
    if (year, month) < (today.year, today.month):
        return ERR_EXPIRED
    return None


def validate_address(address) -> List[str]:
    """Validate street, city, state and zip; return the list of errors."""
    if not isinstance(address, dict) or not address:
        return [ERR_NO_ADDRESS]
    errors = []
    if not _text(address.get("street")):
        errors.append(ERR_STREET)
    if not _text(address.get("city")):
        errors.append(ERR_CITY)
    if address.get("state") not in US_STATES:
        errors.append(ERR_STATE)
    zip_code = address.get("zip")
    if not isinstance(zip_code, str) or not ZIP_RE.match(zip_code):
        errors.append(ERR_ZIP)
    return errors


def validate_credit_card(card, today: Optional[date] = None) -> List[str]:
    """Validate number (Luhn), expiration and CVV; return the list of errors."""
    if not isinstance(card, dict) or not card:
        return [ERR_NO_CARD]
    errors = []
    if not luhn_check(card.get("number")):
        errors.append(ERR_CARD_NUMBER)
    expiration_error = validate_expiration(card.get("expiration"), today)
    if expiration_error:
        errors.append(expiration_error)
    cvv = card.get("cvv")
    if not isinstance(cvv, str) or not CVV_RE.match(cvv):
        errors.append(ERR_CVV)
    return errors


def validate_customer(customer: Dict, today: Optional[date] = None) -> Dict:
    """Validate a whole customer record.

    Returns {"is_valid": bool, "errors": [str, ...]}. Errors are reported in a
    stable order: email, phone, address, credit card.
    """
    customer = customer if isinstance(customer, dict) else {}
    errors: List[str] = []
    if not validate_email(customer.get("email")):
        errors.append(ERR_EMAIL)
    if not validate_phone(customer.get("phone")):
        errors.append(ERR_PHONE)
    errors.extend(validate_address(customer.get("billing_address")))
    errors.extend(validate_credit_card(customer.get("credit_card"), today))
    return {"is_valid": not errors, "errors": errors}
