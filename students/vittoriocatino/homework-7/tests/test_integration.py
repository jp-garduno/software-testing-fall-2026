"""Replay external workflows through validation, pricing, payment and confirmation."""

from datetime import date
from pathlib import Path
from unittest.mock import Mock, call

import pytest

from data_loader import load_workflows
from order_processor import OrderProcessor

DATA = load_workflows(
    Path(__file__).resolve().parents[1] / "test_data/order_workflows.json"
)


@pytest.mark.parametrize("flow", DATA["workflows"], ids=lambda flow: flow["name"])
def test_order_workflow(flow):
    """Compare every step output and assert exact simulated payment calls."""
    payment = Mock(return_value=flow["payment_approved"])
    processor = OrderProcessor(
        payment, date.fromisoformat(DATA["reference_date"]), flow["order_id"]
    )
    for step in flow["steps"]:
        action = step["action"]
        if action == "validate_customer":
            result = processor.validate(step["data"])
        elif action == "create_order":
            result = processor.create(step["data"])
        elif action == "calculate_total":
            result = processor.total()
        elif action == "process_payment":
            result = processor.pay()
        else:
            result = processor.confirmation()
        assert result == step["expected"], action
    assert payment.call_args_list == [
        call(amount) for amount in flow["expected_payment_calls"]
    ]
