"""Integration tests: JSON-described end-to-end order workflows."""

import pytest

from data_loader import case_ids, load_workflows
from order_workflow import OrderWorkflow, WorkflowError

REFERENCE_DATE, WORKFLOWS = load_workflows()


def test_json_has_required_workflows():
    assert len(WORKFLOWS) >= 3


@pytest.mark.parametrize("workflow", WORKFLOWS, ids=case_ids(WORKFLOWS, "name"))
def test_workflow(workflow):
    """Run each step in order; every key in ``expected`` must match the result."""
    engine = OrderWorkflow(today=REFERENCE_DATE)
    for number, step in enumerate(workflow["steps"], start=1):
        result = engine.execute(step["action"], step.get("data"))
        for key, expected in step["expected"].items():
            where = f"{workflow['name']} step {number} ({step['action']}): {key}"
            assert key in result, where
            if isinstance(expected, float):
                assert result[key] == pytest.approx(expected, abs=0.005), where
            else:
                assert result[key] == expected, where


# ---- engine guard rails not reachable through the happy-path JSON ------
def test_unknown_action_raises():
    with pytest.raises(WorkflowError):
        OrderWorkflow().execute("teleport")


def test_steps_before_order_exists_are_rejected():
    engine = OrderWorkflow()
    assert engine.execute("apply_discount", {"code": "SAVE10"}) == {
        "applied": False,
        "reason": "no order",
    }
    assert engine.execute("set_shipping", {"distance_km": 5})["status"] == "rejected"
    assert engine.execute("calculate_total")["status"] == "rejected"


def test_creating_a_new_order_resets_payment_state():
    engine = OrderWorkflow(today=REFERENCE_DATE)
    customer = {
        "email": "a@b.com",
        "phone": "(555) 123-4567",
        "billing_address": {"street": "1 St", "city": "X", "state": "TX", "zip": "75001"},
        "credit_card": {"number": "4111111111111111", "expiration": "12/2030", "cvv": "123"},
    }
    items = [{"name": "A", "price": 10, "quantity": 1, "weight": 0}]
    engine.execute("validate_customer", customer)
    engine.execute("create_order", {"items": items})
    engine.execute("calculate_total")
    assert engine.execute("process_payment")["status"] == "success"
    engine.execute("create_order", {"items": items})
    assert engine.execute("confirm_order")["status"] == "rejected"
