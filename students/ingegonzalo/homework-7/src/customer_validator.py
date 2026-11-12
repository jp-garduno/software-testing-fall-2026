"""Validacion de datos de cliente: email, telefono, direccion y tarjeta."""
import re
from datetime import date
from typing import Dict, Optional

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_RE = re.compile(r"^\([0-9]{3}\) [0-9]{3}-[0-9]{4}$")  # (XXX) XXX-XXXX
ZIP_RE = re.compile(r"^[0-9]{5}(-[0-9]{4})?$")
CARD_RE = re.compile(r"^[0-9]{13,19}$")
EXPIRATION_RE = re.compile(r"^(0[1-9]|1[0-2])/([0-9]{4})$")  # MM/YYYY
CVV_RE = re.compile(r"^[0-9]{3,4}$")

US_STATES = frozenset(
    "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO "
    "MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split()
)


def _text(value) -> str:
    return value.strip() if isinstance(value, str) else ""


def is_valid_email(email) -> bool:
    return bool(EMAIL_RE.match(_text(email)))


def is_valid_phone(phone) -> bool:
    return bool(PHONE_RE.match(_text(phone)))


def luhn_check(number: str) -> bool:
    """Algoritmo de Luhn: duplica cada segundo digito desde la derecha."""
    if not CARD_RE.match(number):
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


def check_expiration(expiration, today: date) -> Optional[str]:
    """Devuelve un mensaje de error o None si la fecha es valida y vigente."""
    match = EXPIRATION_RE.match(_text(expiration))
    if not match:
        return "Invalid expiration date format"
    month, year = int(match.group(1)), int(match.group(2))
    # La tarjeta es valida hasta el final del mes de expiracion
    if (year, month) < (today.year, today.month):
        return "Credit card expired"
    return None


def validate_customer(customer: Dict, today: Optional[date] = None) -> Dict:
    """
    Valida un cliente completo.

    Returns:
        {"is_valid": bool, "errors": [str, ...]}
        Orden de errores: email, telefono, calle, ciudad, estado, zip,
        numero de tarjeta, expiracion, cvv.
    """
    today = today or date.today()
    customer = customer if isinstance(customer, dict) else {}
    address = customer.get("billing_address")
    address = address if isinstance(address, dict) else {}
    card = customer.get("credit_card")
    card = card if isinstance(card, dict) else {}

    errors = []

    if not is_valid_email(customer.get("email")):
        errors.append("Invalid email format")
    if not is_valid_phone(customer.get("phone")):
        errors.append("Invalid phone format")

    if not _text(address.get("street")):
        errors.append("Street is required")
    if not _text(address.get("city")):
        errors.append("City is required")
    if _text(address.get("state")) not in US_STATES:
        errors.append("Invalid state")
    if not ZIP_RE.match(_text(address.get("zip"))):
        errors.append("Invalid zip code")

    if not luhn_check(_text(card.get("number"))):
        errors.append("Invalid credit card number")
    expiration_error = check_expiration(card.get("expiration"), today)
    if expiration_error:
        errors.append(expiration_error)
    if not CVV_RE.match(_text(card.get("cvv"))):
        errors.append("Invalid CVV")

    return {"is_valid": not errors, "errors": errors}