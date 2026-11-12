"""Run fixture-defined checkout flows against the order processor."""

from datetime import date

import pytest

from src.order_processor import OrderProcessor
from tests.data_loader import json_cases


@pytest.mark.parametrize("workflow", json_cases("order_workflows.json", workflows=True))
def test_order_workflow(workflow):
    """Check all step results and amounts sent to the simulated payment gateway."""
    responses = iter(workflow["payment_responses"])
    charges = []

    def charge(amount):
        charges.append(amount)
        return next(responses)

    processor = OrderProcessor(
        workflow["order_id"], charge, today=date.fromisoformat(workflow["as_of"])
    )
    for step in workflow["steps"]:
        result = getattr(processor, step["action"])(**step.get("data", {}))
        assert result == step["expected"], step["action"]
    assert charges == workflow["expected_charges"]
    assert next(responses, None) is None
