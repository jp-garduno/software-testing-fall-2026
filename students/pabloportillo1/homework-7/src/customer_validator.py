import re
from dataclasses import dataclass
from datetime import date

EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9_%+-]+(\.[A-Za-z0-9_%+-]+)*@([A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}"
)
PHONE_PATTERN = re.compile(r"\(\d{3}\) \d{3}-\d{4}")
CITY_PATTERN = re.compile(r"[A-Za-z]+([ '.-]+[A-Za-z]+)*\.?")
ZIP_PATTERN = re.compile(r"\d{5}(-\d{4})?")
CARD_NUMBER_PATTERN = re.compile(r"\d{13,19}")
EXPIRATION_PATTERN = re.compile(r"(0[1-9]|1[0-2])/(\d{4})")
AMEX_PREFIXES = ("34", "37")
US_STATES = frozenset(
    "AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND "
    "OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split()
)


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]

    @property
    def is_valid(self):
        return not self.errors


def validate_customer(customer, today=None):
    """Validate every field and return all errors, in the order email, phone, address, credit card."""
    today = today or date.today()
    errors = [
        _check_format(customer.get("email"), EMAIL_PATTERN, "Email is required", "Invalid email format"),
        _check_format(customer.get("phone"), PHONE_PATTERN, "Phone number is required", "Invalid phone number format"),
        *_address_errors(customer.get("billing_address")),
        *_credit_card_errors(customer.get("credit_card"), today),
    ]
    return ValidationResult(tuple(error for error in errors if error))


def _is_blank(value):
    return value is None or (isinstance(value, str) and not value.strip())


def _check_format(value, pattern, required_message, invalid_message):
    if _is_blank(value):
        return required_message
    if not isinstance(value, str) or not pattern.fullmatch(value):
        return invalid_message
    return None


def _address_errors(address):
    if not isinstance(address, dict):
        return ["Billing address is required"]
    state = address.get("state")
    return [
        "Street is required" if _is_blank(address.get("street")) else None,
        _check_format(address.get("city"), CITY_PATTERN, "City is required", "Invalid city name"),
        "State is required" if _is_blank(state) else (None if state in US_STATES else "Invalid state code"),
        _check_format(address.get("zip"), ZIP_PATTERN, "ZIP code is required", "Invalid ZIP code"),
    ]


def _credit_card_errors(card, today):
    if not isinstance(card, dict):
        return ["Credit card is required"]
    number = card.get("number")
    digits = re.sub(r"[ -]", "", number) if isinstance(number, str) else number
    return [
        _card_number_error(digits),
        _expiration_error(card.get("expiration"), today),
        _cvv_error(card.get("cvv"), digits),
    ]


def _card_number_error(digits):
    if _is_blank(digits):
        return "Credit card number is required"
    if not isinstance(digits, str) or not CARD_NUMBER_PATTERN.fullmatch(digits) or not _passes_luhn(digits):
        return "Invalid credit card number"
    return None


def _passes_luhn(digits):
    total = 0
    for position, digit in enumerate(int(char) for char in reversed(digits)):
        if position % 2 == 1:
            digit = digit * 2 - 9 if digit > 4 else digit * 2
        total += digit
    return total % 10 == 0


def _expiration_error(expiration, today):
    if _is_blank(expiration):
        return "Expiration date is required"
    match = EXPIRATION_PATTERN.fullmatch(expiration) if isinstance(expiration, str) else None
    if match is None:
        return "Invalid expiration date format"
    if (int(match.group(2)), int(match.group(1))) < (today.year, today.month):
        return "Credit card is expired"
    return None


def _cvv_error(cvv, digits):
    if _is_blank(cvv):
        return "CVV is required"
    is_amex = isinstance(digits, str) and digits.startswith(AMEX_PREFIXES)
    expected_length = 4 if is_amex else 3
    if not isinstance(cvv, str) or not re.fullmatch(rf"\d{{{expected_length}}}", cvv):
        return "Invalid CVV"
    return None
