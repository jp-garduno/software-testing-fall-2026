"""Genera test_data/customer_validation.json a partir de un cliente base."""
import copy
import json
from pathlib import Path

BASE = {
    "email": "john@example.com",
    "phone": "(555) 123-4567",
    "billing_address": {"street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001"},
    "credit_card": {"number": "4532015112830366", "expiration": "12/2099", "cvv": "123"},
}


def make(category, name, errors, **overrides):
    customer = copy.deepcopy(BASE)
    for key, value in overrides.items():
        if key in ("email", "phone"):
            customer[key] = value
        elif key in ("street", "city", "state", "zip"):
            customer["billing_address"][key] = value
        elif key in ("number", "expiration", "cvv"):
            customer["credit_card"][key] = value
        else:
            raise KeyError(key)
    return {
        "test_name": name,
        "category": category,
        "customer": customer,
        "expected": {"is_valid": not errors, "errors": errors},
    }


EMAIL, PHONE = "Invalid email format", "Invalid phone format"
STREET, CITY = "Street is required", "City is required"
STATE, ZIP = "Invalid state", "Invalid zip code"
CARD, EXPIRED = "Invalid credit card number", "Credit card expired"
EXP_FMT, CVV = "Invalid expiration date format", "Invalid CVV"

CASES = [
    # --- Valid (3) ---
    make("valid", "valid_customer_all_fields", []),
    make("valid", "valid_customer_zip_plus4", [], zip="10001-1234"),
    make("valid", "valid_customer_amex_four_digit_cvv", [], number="378282246310005", cvv="1234"),
    # --- Invalid email (4) ---
    make("invalid_email", "email_without_at_sign", [EMAIL], email="invalid-email"),
    make("invalid_email", "email_without_domain", [EMAIL], email="user@"),
    make("invalid_email", "email_without_local_part", [EMAIL], email="@example.com"),
    make("invalid_email", "email_with_space", [EMAIL], email="john doe@example.com"),
    # --- Invalid phone (4) ---
    make("invalid_phone", "phone_digits_only", [PHONE], phone="5551234567"),
    make("invalid_phone", "phone_with_dashes", [PHONE], phone="555-123-4567"),
    make("invalid_phone", "phone_wrong_grouping", [PHONE], phone="(555) 1234-567"),
    make("invalid_phone", "phone_short_area_code", [PHONE], phone="(55) 123-4567"),
    # --- Invalid address (5) ---
    make("invalid_address", "address_empty_street", [STREET], street=""),
    make("invalid_address", "address_empty_city", [CITY], city=""),
    make("invalid_address", "address_unknown_state", [STATE], state="XX"),
    make("invalid_address", "address_short_zip", [ZIP], zip="1234"),
    make("invalid_address", "address_letters_in_zip", [ZIP], zip="ABCDE"),
    # --- Invalid credit card (8) ---
    make("invalid_card", "card_fails_luhn", [CARD], number="4532015112830367"),
    make("invalid_card", "card_with_dashes", [CARD], number="4532-0151-1283-0366"),
    make("invalid_card", "card_too_short", [CARD], number="4111"),
    make("invalid_card", "card_too_long", [CARD], number="45320151128303660000"),
    make("invalid_card", "card_expired", [EXPIRED], expiration="01/2020"),
    make("invalid_card", "card_month_13", [EXP_FMT], expiration="13/2099"),
    make("invalid_card", "card_two_digit_year", [EXP_FMT], expiration="12/99"),
    make("invalid_card", "card_cvv_too_short", [CVV], cvv="12"),
    # --- Multiple errors (6) ---
    make("multiple_errors", "multi_email_and_phone", [EMAIL, PHONE], email="bad", phone="123"),
    make("multiple_errors", "multi_whole_address", [STREET, CITY, STATE, ZIP],
         street="", city="", state="XX", zip="1"),
    make("multiple_errors", "multi_whole_card", [CARD, EXPIRED, CVV],
         number="1234567890123456", expiration="01/2020", cvv="1"),
    make("multiple_errors", "multi_email_phone_zip", [EMAIL, PHONE, ZIP],
         email="a@b", phone="x", zip="0"),
    make("multiple_errors", "multi_phone_and_luhn", [PHONE, CARD],
         phone="555-123-4567", number="4532015112830367"),
    make("multiple_errors", "multi_everything_invalid",
         [EMAIL, PHONE, STREET, CITY, STATE, ZIP, CARD, EXP_FMT, CVV],
         email="x", phone="1", street="", city="", state="", zip="",
         number="", expiration="", cvv=""),
]

if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "test_data" / "customer_validation.json"
    out.write_text(json.dumps(CASES, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(CASES)} casos escritos en {out}")