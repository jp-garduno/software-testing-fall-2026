from datetime import date

import pytest

from data_loader import load_workflows
from src.order_workflow import OrderWorkflow

FIXED_TODAY = date(2026, 1, 15)


def _matches(actual, expected):
    if isinstance(expected, float):
        return actual == pytest.approx(expected, abs=0.01)
    return actual == expected


@pytest.mark.parametrize("workflow", load_workflows())
def test_workflow(workflow):
    flow = OrderWorkflow(today=FIXED_TODAY)
    for number, step in enumerate(workflow["steps"], start=1):
        result = flow.execute(step["action"], step.get("data"))
        for key, expected in step["expected"].items():
            assert _matches(result.get(key), expected), (
                f"{workflow['name']} step {number} ({step['action']}): "
                f"'{key}' expected {expected!r}, got {result.get(key)!r}"
            )


def test_minimum_workflows():
    assert len(load_workflows()) >= 3


def test_unknown_action_raises():
    with pytest.raises(ValueError):
        OrderWorkflow().execute("teleport")


def test_create_order_rejects_invalid_items():
    flow = OrderWorkflow(today=FIXED_TODAY)
    flow.customer_valid = True
    result = flow.execute("create_order", {"items": [{"name": "X", "price": -5, "quantity": 1}]})
    assert result["status"] == "rejected"


def test_steps_before_order_exists_are_rejected():
    flow = OrderWorkflow()
    assert flow.execute("apply_discount", {"code": "SAVE10"}) == {"applied": False}
    assert flow.execute("set_shipping", {"distance_km": 5}) == {"status": "rejected"}