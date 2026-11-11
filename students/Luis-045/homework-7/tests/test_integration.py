"""Execute the checkout workflows and check each observable result."""

from datetime import date

import pytest

from src.checkout import Checkout

from .data_cases import load_json_cases

DATA = load_json_cases("order_workflows.json")


@pytest.mark.parametrize("workflow", DATA["workflows"], ids=lambda case: case["name"])
def test_order_workflow(workflow):
    """Drive a fresh checkout through all steps in the workflow."""
    checkout = Checkout(
        workflow["order_id"], today=date.fromisoformat(DATA["reference_date"])
    )
    actions = {
        "validate_customer": checkout.validate_customer,
        "create_order": checkout.create_order,
        "calculate_total": checkout.calculate_total,
        "process_payment": checkout.process_payment,
        "confirm_order": checkout.confirm_order,
    }

    for index, step in enumerate(workflow["steps"], start=1):
        action = actions[step["action"]]
        data = step.get("data", {})
        description = f"{workflow['name']}, step {index} ({step['action']})"
        if "expected_error" in step:
            with pytest.raises(ValueError) as error:
                action(**data)
            assert str(error.value) == step["expected_error"], description
        else:
            assert action(**data) == step["expected"], description
