"""Customer validation: email, phone, billing address and credit card."""

from datetime import date
from typing import Any, Dict, List, Optional

from src import validation_rules as rules

ERR_EMAIL = "Invalid email format"
ERR_PHONE = "Invalid phone format"
ERR_STREET = "Invalid street address"
ERR_CITY = "Invalid city"
ERR_STATE = "Invalid state"
ERR_ZIP = "Invalid zip code"
ERR_CARD_NUMBER = "Invalid credit card number"
ERR_EXPIRATION_FORMAT = "Invalid expiration date format"
ERR_EXPIRED = "Credit card expired"
ERR_CVV = "Invalid CVV"


def _section(customer: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = customer.get(key)
    return value if isinstance(value, dict) else {}


def _address_errors(address: Dict[str, Any]) -> List[str]:
    checks = (
        (rules.is_non_empty_text(address.get("street")), ERR_STREET),
        (rules.is_non_empty_text(address.get("city")), ERR_CITY),
        (rules.is_valid_state(address.get("state")), ERR_STATE),
        (rules.is_valid_zip(address.get("zip")), ERR_ZIP),
    )
    return [message for ok, message in checks if not ok]


def _card_errors(card: Dict[str, Any], today: date) -> List[str]:
    errors = []
    if not rules.is_valid_card_number(card.get("number")):
        errors.append(ERR_CARD_NUMBER)
    expiration = rules.parse_expiration(card.get("expiration"))
    if expiration is None:
        errors.append(ERR_EXPIRATION_FORMAT)
    elif rules.is_expired(*expiration, today):
        errors.append(ERR_EXPIRED)
    if not rules.is_valid_cvv(card.get("cvv")):
        errors.append(ERR_CVV)
    return errors


def validate_customer(
    customer: Dict[str, Any], today: Optional[date] = None
) -> Dict[str, Any]:
    """
    Validate a customer record.

    Args:
        customer: {"email", "phone", "billing_address": {street, city, state, zip},
            "credit_card": {number, expiration "MM/YYYY", cvv}}. Missing parts count as invalid;
            a non-dict customer is treated as an empty record.
        today: reference date for the expiration check (defaults to the real current date).

    Returns:
        {"is_valid": bool, "errors": [messages]} - errors are listed in a stable order:
        email, phone, address, card number, expiration, CVV.
    """
    record = customer if isinstance(customer, dict) else {}
    errors: List[str] = []
    if not rules.is_valid_email(record.get("email")):
        errors.append(ERR_EMAIL)
    if not rules.is_valid_phone(record.get("phone")):
        errors.append(ERR_PHONE)
    errors += _address_errors(_section(record, "billing_address"))
    errors += _card_errors(_section(record, "credit_card"), today or date.today())
    return {"is_valid": not errors, "errors": errors}
