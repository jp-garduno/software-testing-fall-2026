"""Data-driven integration tests (Part 4).

Each workflow in test_data/order_workflows.json is a list of steps. A step
names an ``OrderProcessor`` method, the keyword arguments to call it with and
the fields its result must contain. Only the listed fields are compared, so a
workflow states what matters at that step and nothing more.
"""

import pytest

from src.data_loader import load_workflows
from src.order_processor import OrderProcessor

WORKFLOWS = load_workflows()


def assert_contains(actual, expected, where):
    """Every expected key is present in the result with the same value (floats to the cent)."""
    for key, value in expected.items():
        assert key in actual, f"{where}: result has no '{key}' (got {actual})"
        if isinstance(value, float):
            assert actual[key] == pytest.approx(value, abs=0.001), f"{where}: {key}"
        else:
            assert actual[key] == value, f"{where}: {key}"


@pytest.mark.parametrize("workflow", WORKFLOWS, ids=lambda workflow: workflow.name)
def test_order_workflow(workflow):
    processor = OrderProcessor(today=workflow.reference_date)

    for number, step in enumerate(workflow.steps, start=1):
        result = getattr(processor, step["action"])(**step.get("data", {}))
        assert_contains(result, step["expected"], f"{workflow.name} step {number} ({step['action']})")


def test_at_least_three_workflows():
    assert len(WORKFLOWS) >= 3


def test_every_workflow_reaches_a_payment_attempt():
    for workflow in WORKFLOWS:
        assert "process_payment" in [step["action"] for step in workflow.steps], workflow.name
