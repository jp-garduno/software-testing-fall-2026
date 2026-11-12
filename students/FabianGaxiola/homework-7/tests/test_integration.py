"""Data-driven end-to-end order workflows."""

from datetime import date

import pytest
from data_loaders import load_customer_cases, load_workflows
from order_processor import OrderProcessor


def _run_step(processor, step):
    action = step["action"]
    if action == "validate_customer":
        return processor.validate_customer(step["data"])
    if action == "create_order":
        return processor.create_order(step["data"])
    if action == "calculate_total":
        return processor.calculate_total()
    if action == "process_payment":
        return processor.process_payment(step["data"].get("approved", True))
    raise AssertionError(f"Unknown workflow action: {action}")


@pytest.mark.parametrize(
    "workflow", load_workflows(), ids=lambda workflow: workflow["name"]
)
def test_order_workflow_from_json(workflow):
    processor = OrderProcessor(today=date(2026, 11, 11))

    for step in workflow["steps"]:
        actual = _run_step(processor, step)
        for field, expected in step["expected"].items():
            if isinstance(expected, (int, float)) and not isinstance(expected, bool):
                assert actual[field] == pytest.approx(expected, abs=0.001)
            else:
                assert actual[field] == expected


def test_payment_is_blocked_until_customer_and_order_are_valid():
    processor = OrderProcessor(today=date(2026, 11, 11))
    assert processor.process_payment() == {"status": "blocked"}
    assert processor.calculate_total() == {"status": "blocked"}


def test_create_order_rejects_non_object_data():
    processor = OrderProcessor(today=date(2026, 11, 11))
    customer = load_customer_cases()[0]["customer"]
    processor.validate_customer(customer)

    with pytest.raises(ValueError, match="order data"):
        processor.create_order([])
