"""
Customer Validator - E-Commerce Order Processing

Valida la informacion de un cliente:
    - Email
    - Telefono (formato US: (XXX) XXX-XXXX)
    - Direccion de facturacion (street, city, state, zip)
    - Tarjeta de credito (algoritmo de Luhn, expiracion MM/YYYY, CVV)

Uso:
    result = validate_customer(customer)
    # {"is_valid": bool, "errors": [str, ...]}

Los errores siempre salen en el mismo orden:
    email -> telefono -> direccion -> tarjeta
para que los tests puedan comparar la lista exacta.
"""

import re
from datetime import date
from typing import Dict, List, Optional

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")
PHONE_PATTERN = re.compile(r"^\(\d{3}\) \d{3}-\d{4}$")
ZIP_PATTERN = re.compile(r"^\d{5}(-\d{4})?$")
EXPIRATION_PATTERN = re.compile(r"^(0[1-9]|1[0-2])/(\d{4})$")
CVV_PATTERN = re.compile(r"^\d{3,4}$")

US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC",
}


# ---------------------------------------------------------------------------
# Validadores individuales: cada uno regresa una lista de errores (vacia = ok)
# ---------------------------------------------------------------------------

def validate_email(email: Optional[str]) -> List[str]:
    """Valida formato usuario@dominio.tld, sin espacios ni puntos dobles."""
    if not email:
        return ["Missing email"]
    if ".." in email or not EMAIL_PATTERN.match(email):
        return ["Invalid email format"]
    return []


def validate_phone(phone: Optional[str]) -> List[str]:
    """Valida formato US exacto: (XXX) XXX-XXXX."""
    if not phone:
        return ["Missing phone"]
    if not PHONE_PATTERN.match(phone):
        return ["Invalid phone format"]
    return []


def validate_address(address: Optional[Dict]) -> List[str]:
    """Valida que existan street y city, estado US valido y zip de 5 (o 5+4) digitos."""
    if not address:
        return ["Missing billing address"]

    errors = []
    if not str(address.get("street", "")).strip():
        errors.append("Missing street")
    if not str(address.get("city", "")).strip():
        errors.append("Missing city")
    if address.get("state") not in US_STATES:
        errors.append("Invalid state")
    if not ZIP_PATTERN.match(str(address.get("zip", ""))):
        errors.append("Invalid zip code")
    return errors


def luhn_check(number: str) -> bool:
    """
    Algoritmo de Luhn.
    De derecha a izquierda, duplica cada segundo digito (si pasa de 9, resta 9).
    El numero es valido si la suma total es multiplo de 10.
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
    """Formato MM/YYYY; la tarjeta es valida hasta el ultimo dia de ese mes."""
    today = today or date.today()
    match = EXPIRATION_PATTERN.match(expiration or "")
    if not match:
        return ["Invalid expiration format"]

    month, year = int(match.group(1)), int(match.group(2))
    if (year, month) < (today.year, today.month):
        return ["Credit card expired"]
    return []


def validate_credit_card(card: Optional[Dict], today: Optional[date] = None) -> List[str]:
    """Valida numero (13-19 digitos + Luhn), expiracion y CVV (3 o 4 digitos)."""
    if not card:
        return ["Missing credit card"]

    errors = []
    # Se permiten espacios y guiones como separadores: "4532 0151 1283 0366"
    number = str(card.get("number", "")).replace(" ", "").replace("-", "")
    if not (13 <= len(number) <= 19) or not luhn_check(number):
        errors.append("Invalid credit card number")

    errors.extend(validate_expiration(card.get("expiration"), today))

    if not CVV_PATTERN.match(str(card.get("cvv", ""))):
        errors.append("Invalid CVV")
    return errors


# ---------------------------------------------------------------------------
# Validador principal
# ---------------------------------------------------------------------------

def validate_customer(customer: Dict, today: Optional[date] = None) -> Dict:
    """
    Valida todos los campos del cliente.

    Args:
        customer: dict con email, phone, billing_address y credit_card
        today: fecha de referencia para la expiracion (por defecto, hoy)

    Returns:
        {"is_valid": bool, "errors": [str, ...]}
    """
    errors = []
    errors += validate_email(customer.get("email"))
    errors += validate_phone(customer.get("phone"))
    errors += validate_address(customer.get("billing_address"))
    errors += validate_credit_card(customer.get("credit_card"), today)

    return {"is_valid": len(errors) == 0, "errors": errors}
