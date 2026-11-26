"""End-to-end workflow tests driven by test_data/order_workflows.json."""
import json
from datetime import date

import pytest

from data_loader import DATA_DIR
from order_processor import OrderWorkflow

with open(DATA_DIR / "order_workflows.json") as handle:
    SPEC = json.load(handle)

REFERENCE_DATE = date.fromisoformat(SPEC["reference_date"])
WORKFLOWS = SPEC["workflows"]


def assert_subset(expected, actual, context):
    """Every key in ``expected`` must match ``actual`` (floats to the cent)."""
    for key, value in expected.items():
        assert key in actual, f"{context}: missing key '{key}' in {actual}"
        if isinstance(value, float):
            assert actual[key] == pytest.approx(value, abs=0.005), f"{context}: {key}"
        else:
            assert actual[key] == value, f"{context}: {key}"


@pytest.mark.parametrize("workflow", WORKFLOWS, ids=[w["name"] for w in WORKFLOWS])
def test_workflow(workflow):
    engine = OrderWorkflow(today=REFERENCE_DATE)
    for number, step in enumerate(workflow["steps"], 1):
        result = engine.execute(step["action"], step.get("data"))
        assert_subset(step["expected"], result, f"step {number} ({step['action']})")


def test_at_least_three_workflows():
    assert len(WORKFLOWS) >= 3


def test_confirmation_contains_reference_number():
    engine = OrderWorkflow(today=REFERENCE_DATE)
    complete = WORKFLOWS[0]
    for step in complete["steps"]:
        result = engine.execute(step["action"], step.get("data"))
    assert result["confirmation_number"].startswith("ORD-")
    assert result["email"] == "john@example.com"


def test_unknown_action_raises():
    with pytest.raises(ValueError):
        OrderWorkflow(today=REFERENCE_DATE).execute("teleport")


@pytest.mark.parametrize("action", [
    "apply_discount", "set_shipping", "calculate_total",
    "process_payment", "generate_confirmation",
])
def test_steps_without_order_are_rejected(action):
    result = OrderWorkflow(today=REFERENCE_DATE).execute(action, {})
    assert result == {"status": "rejected", "reason": "no active order"}


def test_create_order_edge_cases():
    customer = WORKFLOWS[0]["steps"][0]["data"]
    engine = OrderWorkflow(today=REFERENCE_DATE)
    engine.execute("validate_customer", customer)
    assert engine.execute("create_order", {"items": []})["reason"] == "order has no items"
    bad = engine.execute("create_order", {"items": [{"price": -1, "quantity": 1}]})
    assert bad["status"] == "rejected"


def test_set_shipping_rejects_negative_distance():
    customer = WORKFLOWS[0]["steps"][0]["data"]
    engine = OrderWorkflow(today=REFERENCE_DATE)
    engine.execute("validate_customer", customer)
    engine.execute("create_order", {"items": [{"price": 5, "quantity": 1}]})
    assert engine.execute("set_shipping", {"distance_km": -5})["status"] == "rejected"


def test_zero_total_payment_is_declined():
    customer = WORKFLOWS[0]["steps"][0]["data"]
    engine = OrderWorkflow(today=REFERENCE_DATE)
    engine.execute("validate_customer", customer)
    engine.execute("create_order", {"items": [{"price": 0, "quantity": 1}]})
    assert engine.execute("process_payment")["reason"] == "invalid amount"
