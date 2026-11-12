"""
Integration Test Suite - E-Commerce Order Workflows.

Tests complete multi-step end-to-end workflows defined in test_data/order_workflows.json:
customer validation -> order creation -> discount application -> shipping -> total calculation -> payment.
"""

import os
import json
from datetime import date
import pytest
from src.order_calculator import Order
from src.customer_validator import validate_customer


def load_order_workflows():
    """Load workflows from test_data/order_workflows.json."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, "test_data", "order_workflows.json")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [(wf["name"], wf["steps"]) for wf in data["workflows"]]


@pytest.mark.parametrize(
    "workflow_name,steps",
    load_order_workflows(),
    ids=lambda val: val if isinstance(val, str) else "",
)
def test_order_workflow_integration(workflow_name, steps):
    """Execute end-to-end multi-step order workflows."""
    context = {
        "customer": None,
        "order": None,
        "customer_valid": False,
        "total_breakdown": None,
        "payment_processed": False,
        "aborted": False,
    }

    ref_date = date(2026, 11, 1)

    for step in steps:
        action = step["action"]
        expected = step["expected"]

        if action == "validate_customer":
            context["customer"] = step["data"]
            val_result = validate_customer(context["customer"], today=ref_date)
            context["customer_valid"] = val_result["is_valid"]
            assert val_result["is_valid"] == expected["is_valid"], f"{workflow_name}: customer validity mismatch"
            assert val_result["errors"] == expected["errors"], f"{workflow_name}: customer error list mismatch"

            if not val_result["is_valid"]:
                context["aborted"] = True

        elif action == "order_aborted":
            assert context["aborted"] is True
            assert expected["status"] == "rejected"

        elif action == "create_order":
            assert context["customer_valid"] is True, "Cannot create order with invalid customer"
            data = step["data"]
            order = Order(items=data["items"], customer_type=data.get("customer_type", "regular"))
            context["order"] = order
            assert expected["status"] == "created"
            assert order.calculate_subtotal() == pytest.approx(expected["subtotal"], abs=0.01)

        elif action == "apply_discount":
            order = context["order"]
            code = step["data"]["code"]
            applied = order.apply_discount(code)
            assert applied == expected["applied"]
            assert order.calculate_discount() == pytest.approx(expected["discount_amount"], abs=0.01)

        elif action == "set_shipping":
            order = context["order"]
            dist = step["data"]["distance_km"]
            is_express = step["data"].get("is_express", False)
            order.set_shipping(dist, is_express)
            assert order.calculate_shipping() == pytest.approx(expected["shipping_cost"], abs=0.01)

        elif action == "calculate_total":
            order = context["order"]
            totals = order.calculate_total()
            context["total_breakdown"] = totals

            for k in ("subtotal", "discount", "tax", "shipping", "total"):
                assert totals[k] == pytest.approx(expected[k], abs=0.01), f"{workflow_name}: mismatch in {k}"

        elif action == "process_payment":
            assert context["total_breakdown"] is not None
            charged = context["total_breakdown"]["total"]
            assert charged == pytest.approx(expected["amount_charged"], abs=0.01)
            context["payment_processed"] = True
            assert expected["status"] == "success"

