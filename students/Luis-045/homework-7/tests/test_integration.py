"""Execute the checkout workflows and check each observable result."""

import json
from datetime import date
from pathlib import Path

import pytest

from src.order_calculator import Checkout

DATA_PATH = Path(__file__).resolve().parents[1] / "test_data" / "order_workflows.json"
with DATA_PATH.open(encoding="utf-8") as file:
    DATA = json.load(file)


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
