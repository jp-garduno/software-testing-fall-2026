"""Customer and payment validation module for e-commerce checkout."""

import re
from typing import Any, Dict, List, Tuple

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
PHONE_REGEX = re.compile(r"^\(\d{3}\) \d{3}-\d{4}$")
STATE_REGEX = re.compile(r"^[A-Z]{2}$")
ZIP_REGEX = re.compile(r"^\d{5}(-\d{4})?$")
CVV_REGEX = re.compile(r"^\d{3,4}$")
EXPIRATION_REGEX = re.compile(r"^(0[1-9]|1[0-2])/(\d{4})$")


def validate_email(email: Any) -> bool:
    """Validate email format."""
    if not isinstance(email, str) or not email or " " in email or ".." in email:
        return False
    return bool(EMAIL_REGEX.match(email))


def validate_phone(phone: Any) -> bool:
    """Validate US phone number format: (XXX) XXX-XXXX."""
    if not isinstance(phone, str) or not phone:
        return False
    return bool(PHONE_REGEX.match(phone))


def validate_billing_address(address: Any) -> List[str]:
    """Validate billing address fields (street, city, state, zip)."""
    if not isinstance(address, dict):
        return ["Invalid billing address"]

    errors: List[str] = []
    street = address.get("street", "")
    city = address.get("city", "")
    state = address.get("state", "")
    zip_code = address.get("zip", "")

    if not isinstance(street, str) or len(street.strip()) < 3:
        errors.append("Invalid street address")
    if not isinstance(city, str) or len(city.strip()) < 2:
        errors.append("Invalid city")
    if not isinstance(state, str) or not STATE_REGEX.match(state):
        errors.append("Invalid state code")
    if not isinstance(zip_code, str) or not ZIP_REGEX.match(zip_code):
        errors.append("Invalid zip code")

    return errors


def validate_luhn(card_number: Any) -> bool:
    """Validate a credit card number using the Luhn algorithm."""
    if not isinstance(card_number, str):
        return False

    cleaned = card_number.replace(" ", "").replace("-", "")
    if not cleaned.isdigit() or not 13 <= len(cleaned) <= 19:
        return False

    total = 0
    reverse_digits = cleaned[::-1]
    for index, char in enumerate(reverse_digits):
        digit = int(char)
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0


def validate_expiration(expiration: Any, reference_year_month: Tuple[int, int] = (2025, 1)) -> bool:
    """Validate credit card expiration date in MM/YYYY format against reference (year, month)."""
    if not isinstance(expiration, str):
        return False

    match = EXPIRATION_REGEX.match(expiration)
    if not match:
        return False

    month = int(match.group(1))
    year = int(match.group(2))
    ref_year, ref_month = reference_year_month

    return (year, month) >= (ref_year, ref_month)


def validate_cvv(cvv: Any) -> bool:
    """Validate 3- or 4-digit credit card CVV."""
    if not isinstance(cvv, str):
        return False
    return bool(CVV_REGEX.match(cvv))


def validate_credit_card(
    credit_card: Any, reference_year_month: Tuple[int, int] = (2025, 1)
) -> List[str]:
    """Validate credit card object (number, expiration, cvv)."""
    if not isinstance(credit_card, dict):
        return ["Invalid credit card information"]

    errors: List[str] = []
    if not validate_luhn(credit_card.get("number")):
        errors.append("Invalid credit card number")
    if not validate_expiration(credit_card.get("expiration"), reference_year_month):
        errors.append("Invalid expiration date")
    if not validate_cvv(credit_card.get("cvv")):
        errors.append("Invalid CVV")

    return errors


def validate_customer(
    customer: Dict[str, Any], reference_year_month: Tuple[int, int] = (2025, 1)
) -> Dict[str, Any]:
    """
    Validate complete customer profile including email, phone, billing address, and credit card.

    Returns:
        {"is_valid": bool, "errors": List[str]}
    """
    if not isinstance(customer, dict):
        return {"is_valid": False, "errors": ["Invalid customer data"]}

    errors: List[str] = []

    if not validate_email(customer.get("email")):
        errors.append("Invalid email format")

    if not validate_phone(customer.get("phone")):
        errors.append("Invalid phone format")

    errors.extend(validate_billing_address(customer.get("billing_address")))
    errors.extend(validate_credit_card(customer.get("credit_card"), reference_year_month))

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
    }


def process_order_workflow(workflow: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute an end-to-end order workflow consisting of sequential steps.

    Supported actions:
        - validate_customer
        - create_order
        - calculate_total
        - process_payment
    """
    from order_calculator import Order  # pylint: disable=import-outside-toplevel

    state: Dict[str, Any] = {
        "customer_valid": False,
        "order": None,
        "totals": None,
        "payment_status": "pending",
        "step_results": [],
    }

    for step in workflow.get("steps", []):
        action = step.get("action")
        data = step.get("data", {})

        if action == "validate_customer":
            validation = validate_customer(data)
            state["customer_valid"] = validation["is_valid"]
            state["step_results"].append(
                {
                    "action": action,
                    "valid": validation["is_valid"],
                    "errors": validation["errors"],
                }
            )
        elif action == "create_order":
            order = Order(
                items=data.get("items", []),
                customer_type=data.get("customer_type", "regular"),
            )
            discount_code = data.get("discount_code")
            discount_applied = False
            if discount_code and discount_code != "NONE":
                discount_applied = order.apply_discount(discount_code)
            order.set_shipping(
                distance_km=data.get("distance_km", 0.0),
                is_express=data.get("is_express", False),
            )
            state["order"] = order
            state["step_results"].append(
                {
                    "action": action,
                    "status": "created",
                    "discount_applied": discount_applied,
                }
            )
        elif action == "calculate_total":
            if state["order"] is None:
                state["step_results"].append({"action": action, "error": "No active order"})
            else:
                totals = state["order"].calculate_total()
                state["totals"] = totals
                state["step_results"].append({"action": action, **totals})
        elif action == "process_payment":
            if not state["customer_valid"] or state["totals"] is None or state["totals"]["total"] <= 0:
                state["payment_status"] = "failed"
            else:
                state["payment_status"] = "success"
            state["step_results"].append(
                {"action": action, "status": state["payment_status"]}
            )

    return state
