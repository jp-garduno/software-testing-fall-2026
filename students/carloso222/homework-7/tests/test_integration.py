"""Part 4 - end-to-end workflows loaded from test_data/order_workflows.json."""

from datetime import date

import pytest
from src.order_workflow import OrderWorkflow, run_workflow
from tests.data_loader import load_workflows

_DATA = load_workflows()
_TODAY = date.fromisoformat(_DATA["reference_date"])
_VALID_CUSTOMER = {
    "email": "a@b.com",
    "phone": "(555) 123-4567",
    "billing_address": {
        "street": "1 Main St",
        "city": "Austin",
        "state": "TX",
        "zip": "73301",
    },
    "credit_card": {
        "number": "4111111111111111",
        "expiration": "12/2030",
        "cvv": "123",
    },
}


@pytest.mark.parametrize("workflow", _DATA["workflows"], ids=lambda w: w["name"])
def test_workflow_steps_return_expected_results(workflow):
    results = run_workflow(workflow, today=_TODAY)

    actual = [
        {key: result[key] for key in step["expected"]}
        for step, result in zip(workflow["steps"], results)
    ]
    assert actual == [
        pytest.approx(step["expected"], abs=0.005) for step in workflow["steps"]
    ]


def test_workflow_data_has_at_least_one_failing_payment():
    statuses = [wf["steps"][-1]["expected"].get("status") for wf in _DATA["workflows"]]

    assert "declined" in statuses


def test_run_step_unknown_action_raises_value_error():
    with pytest.raises(ValueError, match="Unknown workflow action"):
        OrderWorkflow(_TODAY).run_step("ship_order")


def test_create_order_missing_items_is_rejected():
    result = OrderWorkflow(_TODAY).create_order({"customer_type": "regular"})

    assert result["status"] == "rejected"


def test_process_payment_without_validation_is_declined():
    flow = OrderWorkflow(_TODAY)
    flow.create_order({"items": [{"name": "x", "price": 5, "quantity": 1}]})

    assert flow.process_payment()["status"] == "declined"


def test_create_order_reports_discount_applied_flag():
    flow = OrderWorkflow(_TODAY)

    result = flow.create_order(
        {
            "items": [{"name": "x", "price": 80, "quantity": 1}],
            "discount_code": "SAVE10",
        }
    )

    assert result == {"status": "created", "discount_applied": True}


def test_process_payment_success_includes_confirmation_message():
    flow = OrderWorkflow(_TODAY)
    flow.validate_customer(_VALID_CUSTOMER)
    flow.create_order({"items": [{"name": "x", "price": 10, "quantity": 1}]})

    result = flow.process_payment()

    assert result["confirmation"] == "Order confirmed, total $10.80"
