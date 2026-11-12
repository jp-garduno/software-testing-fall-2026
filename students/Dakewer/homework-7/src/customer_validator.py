"""Customer validation: email, phone, billing address and credit card.

``validate_customer`` returns ``{"is_valid": bool, "errors": [str, ...]}``.
Errors always appear in this order: email, phone, street, city, state,
zip, card number, expiration, CVV.
"""
import re
from datetime import date
from typing import Dict, List, Optional

ERR_EMAIL = "Invalid email format"
ERR_PHONE = "Invalid phone format"
ERR_STREET = "Invalid street address"
ERR_CITY = "Invalid city"
ERR_STATE = "Invalid state"
ERR_ZIP = "Invalid zip code"
ERR_CARD = "Invalid credit card number"
ERR_EXP_FORMAT = "Invalid expiration date"
ERR_EXPIRED = "Credit card expired"
ERR_CVV = "Invalid CVV"

US_STATES = frozenset(
    "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS "
    "MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV "
    "WI WY DC".split()
)

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}")
_PHONE_RE = re.compile(r"\(\d{3}\) \d{3}-\d{4}")
_CITY_RE = re.compile(r"[A-Za-z][A-Za-z .'-]*")
_ZIP_RE = re.compile(r"\d{5}(-\d{4})?")
_CARD_RE = re.compile(r"\d{13,19}")
_EXP_RE = re.compile(r"(0[1-9]|1[0-2])/(\d{4})")
_CVV_RE = re.compile(r"\d{3,4}")


def _text(value) -> str:
    """Return ``value`` if it is a string, otherwise an empty string."""
    return value if isinstance(value, str) else ""


def is_valid_email(email: str) -> bool:
    email = _text(email)
    if len(email) > 254 or not _EMAIL_RE.fullmatch(email):
        return False
    local, domain = email.rsplit("@", 1)
    if local.startswith(".") or local.endswith(".") or ".." in local:
        return False
    return not any(l.startswith("-") or l.endswith("-") for l in domain.split("."))


def is_valid_phone(phone: str) -> bool:
    """US format: (XXX) XXX-XXXX"""
    return bool(_PHONE_RE.fullmatch(_text(phone)))


def is_valid_street(street: str) -> bool:
    street = _text(street).strip()
    return (
        0 < len(street) <= 100
        and re.search(r"[A-Za-z]", street) is not None
        and re.search(r"\d", street) is not None
    )


def is_valid_city(city: str) -> bool:
    city = _text(city).strip()
    return len(city) <= 60 and bool(_CITY_RE.fullmatch(city))


def is_valid_state(state: str) -> bool:
    return _text(state) in US_STATES


def is_valid_zip(zip_code: str) -> bool:
    return bool(_ZIP_RE.fullmatch(_text(zip_code)))


def luhn_check(number: str) -> bool:
    """Luhn checksum for a string of digits."""
    if not re.fullmatch(r"[0-9]+", number):
        return False
    total = 0
    for position, char in enumerate(reversed(number)):
        digit = int(char)
        if position % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def is_valid_card_number(number: str) -> bool:
    """13-19 digits (spaces/hyphens allowed) that pass the Luhn check."""
    digits = re.sub(r"[ -]", "", _text(number))
    return bool(_CARD_RE.fullmatch(digits)) and luhn_check(digits)


def check_expiration(expiration: str, today: Optional[date] = None) -> Optional[str]:
    """Validate ``MM/YYYY``. A card is good through the end of its month.

    Returns None when valid, otherwise the error message.
    """
    today = today or date.today()
    match = _EXP_RE.fullmatch(_text(expiration))
    if not match:
        return ERR_EXP_FORMAT
    month, year = int(match.group(1)), int(match.group(2))
    if (year, month) < (today.year, today.month):
        return ERR_EXPIRED
    return None


def is_valid_cvv(cvv: str) -> bool:
    return bool(_CVV_RE.fullmatch(_text(cvv)))


def validate_customer(customer: Dict, today: Optional[date] = None) -> Dict:
    """Validate every customer field and collect all errors.

    ``today`` is injectable so tests do not depend on the real date.
    """
    if not isinstance(customer, dict):
        raise ValueError("customer must be a dict")

    address = customer.get("billing_address")
    address = address if isinstance(address, dict) else {}
    card = customer.get("credit_card")
    card = card if isinstance(card, dict) else {}

    errors: List[str] = []
    if not is_valid_email(customer.get("email")):
        errors.append(ERR_EMAIL)
    if not is_valid_phone(customer.get("phone")):
        errors.append(ERR_PHONE)
    if not is_valid_street(address.get("street")):
        errors.append(ERR_STREET)
    if not is_valid_city(address.get("city")):
        errors.append(ERR_CITY)
    if not is_valid_state(address.get("state")):
        errors.append(ERR_STATE)
    if not is_valid_zip(address.get("zip")):
        errors.append(ERR_ZIP)
    if not is_valid_card_number(card.get("number")):
        errors.append(ERR_CARD)
    expiration_error = check_expiration(card.get("expiration"), today)
    if expiration_error:
        errors.append(expiration_error)
    if not is_valid_cvv(card.get("cvv")):
        errors.append(ERR_CVV)

    return {"is_valid": not errors, "errors": errors}
