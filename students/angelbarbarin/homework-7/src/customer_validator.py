"""Customer validation for the e-commerce order processing system (homework 7, part 2).

``validate_customer`` checks every field and returns *all* the problems it finds, in a fixed
order (email, phone, address, credit card), so a test can compare the whole error list.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")
PHONE_PATTERN = re.compile(r"^\(\d{3}\) \d{3}-\d{4}$")
ZIP_PATTERN = re.compile(r"^\d{5}(-\d{4})?$")
EXPIRATION_PATTERN = re.compile(r"^(0[1-9]|1[0-2])/(\d{4})$")
CARD_LENGTHS = range(13, 20)

US_STATES = frozenset(
    "AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY "
    "NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split()
)

# Error messages are part of the contract: the JSON test data compares them literally.
ERR_EMAIL_REQUIRED = "Email is required"
ERR_EMAIL_FORMAT = "Invalid email format"
ERR_PHONE_REQUIRED = "Phone is required"
ERR_PHONE_FORMAT = "Invalid phone format"
ERR_ADDRESS_REQUIRED = "Billing address is required"
ERR_STREET = "Street is required"
ERR_CITY = "City is required"
ERR_STATE = "Invalid state"
ERR_ZIP = "Invalid ZIP code"
ERR_CARD_REQUIRED = "Credit card is required"
ERR_CARD_NUMBER = "Invalid credit card number"
ERR_EXPIRATION_FORMAT = "Invalid expiration date format"
ERR_CARD_EXPIRED = "Credit card is expired"
ERR_CVV = "Invalid CVV"


@dataclass
class ValidationResult:
    """Outcome of a validation: valid only when there are no errors."""

    errors: List[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


def luhn_checksum_ok(number: str) -> bool:
    """Luhn (mod 10) check: double every second digit from the right, sum, must end in 0."""
    total = 0
    for position, char in enumerate(reversed(number)):
        digit = int(char)
        if position % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def normalize_card_number(number: str) -> str:
    """Remove the spaces and dashes people type between digit groups."""
    return re.sub(r"[ -]", "", number or "")


def validate_email(email: Optional[str]) -> List[str]:
    if not email or not str(email).strip():
        return [ERR_EMAIL_REQUIRED]
    return [] if EMAIL_PATTERN.match(str(email).strip()) else [ERR_EMAIL_FORMAT]


def validate_phone(phone: Optional[str]) -> List[str]:
    """US format only: (XXX) XXX-XXXX."""
    if not phone or not str(phone).strip():
        return [ERR_PHONE_REQUIRED]
    return [] if PHONE_PATTERN.match(str(phone).strip()) else [ERR_PHONE_FORMAT]


def validate_address(address: Optional[Dict]) -> List[str]:
    if not isinstance(address, dict) or not address:
        return [ERR_ADDRESS_REQUIRED]
    errors = []
    if not str(address.get("street") or "").strip():
        errors.append(ERR_STREET)
    if not str(address.get("city") or "").strip():
        errors.append(ERR_CITY)
    if str(address.get("state") or "").strip().upper() not in US_STATES:
        errors.append(ERR_STATE)
    if not ZIP_PATTERN.match(str(address.get("zip") or "").strip()):
        errors.append(ERR_ZIP)
    return errors


def validate_credit_card(card: Optional[Dict], today: Optional[date] = None) -> List[str]:
    """Number (13-19 digits + Luhn), expiration MM/YYYY (valid through the end of that month) and CVV."""
    if not isinstance(card, dict) or not card:
        return [ERR_CARD_REQUIRED]
    errors = []

    number = normalize_card_number(str(card.get("number") or ""))
    if not (number.isdigit() and len(number) in CARD_LENGTHS and luhn_checksum_ok(number)):
        errors.append(ERR_CARD_NUMBER)

    match = EXPIRATION_PATTERN.match(str(card.get("expiration") or "").strip())
    if not match:
        errors.append(ERR_EXPIRATION_FORMAT)
    else:
        today = today or date.today()
        month, year = int(match.group(1)), int(match.group(2))
        if (year, month) < (today.year, today.month):
            errors.append(ERR_CARD_EXPIRED)

    # American Express (34xx / 37xx) uses a 4-digit CVV; every other brand uses 3.
    expected_cvv_length = 4 if number[:2] in ("34", "37") else 3
    cvv = str(card.get("cvv") or "")
    if not (cvv.isdigit() and len(cvv) == expected_cvv_length):
        errors.append(ERR_CVV)
    return errors


def validate_customer(customer: Optional[Dict], today: Optional[date] = None) -> ValidationResult:
    """Validate every field of a customer and collect all the errors."""
    customer = customer if isinstance(customer, dict) else {}
    errors = (
        validate_email(customer.get("email"))
        + validate_phone(customer.get("phone"))
        + validate_address(customer.get("billing_address"))
        + validate_credit_card(customer.get("credit_card"), today)
    )
    return ValidationResult(errors)
