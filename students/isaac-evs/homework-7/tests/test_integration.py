"""End-to-end tests: each workflow in test_data/order_workflows.json is executed step by step."""

import pytest
from data_loader import REFERENCE_DATE, load_workflow_file, load_workflows

from order_workflow import OrderWorkflow

CUSTOMERS = load_workflow_file()["customers"]
ITEM = {"name": "Widget", "price": 40, "quantity": 1, "weight": 1}


def new_workflow():
    return OrderWorkflow(today=REFERENCE_DATE)


def resolve(data):
    """Replace a customer name in step data with the customer record it refers to."""
    data = dict(data or {})
    if "customer" in data:
        data["customer"] = CUSTOMERS[data["customer"]]
    return data


def assert_matches(result, expected, label):
    """Every expected key must be present; numbers compare to the cent, everything else exactly."""
    for key, wanted in expected.items():
        assert key in result, f"{label}: missing {key!r} in {result}"
        if isinstance(wanted, (int, float)) and not isinstance(wanted, bool):
            assert result[key] == pytest.approx(wanted, abs=0.005), f"{label}: {key}"
        else:
            assert result[key] == wanted, f"{label}: {key}"


@pytest.mark.parametrize("workflow", load_workflows())
def test_workflow(workflow):
    engine = new_workflow()
    for number, step in enumerate(workflow["steps"], start=1):
        result = engine.execute(step["action"], resolve(step.get("data")))
        assert_matches(result, step["expected"], f"{workflow['name']} step {number} ({step['action']})")


def test_workflow_file_contains_at_least_three_workflows():
    assert len(load_workflows()) >= 3


@pytest.mark.parametrize("action", ["apply_discount", "set_shipping", "calculate_total"])
def test_steps_before_an_order_exists_are_rejected(action):
    data = {"code": "SAVE10", "distance_km": 5}
    assert new_workflow().execute(action, data) == {"status": "rejected", "error": "No order"}


def test_unknown_action_raises():
    with pytest.raises(ValueError, match="Unknown workflow action"):
        new_workflow().execute("ship_to_the_moon")


def test_confirmation_numbers_increase_across_orders():
    engine = new_workflow()
    engine.execute("validate_customer", {"customer": CUSTOMERS["standard"]})
    numbers = []
    for _ in range(2):
        engine.execute("create_order", {"items": [ITEM]})
        engine.execute("calculate_total")
        engine.execute("process_payment")
        numbers.append(engine.execute("generate_confirmation")["confirmation_number"])
    assert numbers == ["ORD-000001", "ORD-000002"]


def test_a_new_order_must_be_priced_and_paid_again():
    engine = new_workflow()
    engine.execute("validate_customer", {"customer": CUSTOMERS["standard"]})
    engine.execute("create_order", {"items": [ITEM]})
    engine.execute("calculate_total")
    engine.execute("process_payment")
    engine.execute("create_order", {"items": [ITEM]})
    assert engine.execute("process_payment")["status"] == "rejected"


def test_confirmation_requires_a_successful_payment():
    engine = new_workflow()
    engine.execute("validate_customer", {"customer": CUSTOMERS["standard"]})
    engine.execute("create_order", {"items": [ITEM]})
    engine.execute("calculate_total")
    assert engine.execute("generate_confirmation")["status"] == "rejected"


def test_workflow_uses_the_real_date_when_none_is_given():
    customer = {
        **CUSTOMERS["standard"],
        "credit_card": {**CUSTOMERS["standard"]["credit_card"], "expiration": "12/2999"},
    }
    assert OrderWorkflow().execute("validate_customer", {"customer": customer}) == {"valid": True, "errors": []}
