"""Data-driven end-to-end workflows (part 4).

test_data/order_workflows.json describes each checkout as a list of steps. The test replays
the steps on one OrderProcessor and checks every key listed in each step's "expected" object.
"""

from datetime import date
from pathlib import Path

import pytest

from data_files import load_workflows
from order_processor import OrderProcessor, SimulatedPaymentGateway

DATA = load_workflows(Path(__file__).resolve().parent.parent / "test_data" / "order_workflows.json")
WORKFLOWS = DATA["workflows"]
REFERENCE_DATE = date.fromisoformat(DATA["reference_date"])


def assert_matches(actual, expected, where):
    """Every expected key must be present; money is compared to the cent."""
    for key, value in expected.items():
        assert key in actual, f"{where}: missing '{key}' in {actual}"
        if isinstance(value, float):
            assert actual[key] == pytest.approx(value, abs=0.005), f"{where}: {key}"
        else:
            assert actual[key] == value, f"{where}: {key} expected {value!r}, got {actual[key]!r}"


@pytest.mark.parametrize("workflow", WORKFLOWS, ids=[workflow["name"] for workflow in WORKFLOWS])
def test_order_workflow(workflow):
    gateway = SimulatedPaymentGateway(**workflow.get("gateway", {}))
    processor = OrderProcessor(gateway, today=REFERENCE_DATE)

    for number, step in enumerate(workflow["steps"], start=1):
        result = processor.run_step(step["action"], step.get("data"))
        assert_matches(result, step["expected"], f"{workflow['name']} step {number} ({step['action']})")


def test_at_least_three_workflows():
    assert len(WORKFLOWS) >= 3


def test_successful_payment_is_recorded_by_gateway():
    workflow = next(w for w in WORKFLOWS if w["name"] == "complete_order_flow")
    gateway = SimulatedPaymentGateway()
    processor = OrderProcessor(gateway, today=REFERENCE_DATE)
    for step in workflow["steps"]:
        processor.run_step(step["action"], step.get("data"))

    assert len(gateway.charges) == 1
    card, amount = gateway.charges[0]
    assert card == "4532015112830366"
    assert amount == processor.breakdown["total"]
    assert processor.status == "paid"


@pytest.mark.parametrize("action", ["_sequence", "run_step", "does_not_exist"])
def test_private_or_unknown_actions_are_refused(action):
    assert OrderProcessor().run_step(action) == {"status": "error", "error": f"Unknown action: {action}"}


def test_invalid_shipping_distance_reports_error():
    processor = OrderProcessor(today=REFERENCE_DATE)
    processor.run_step("validate_customer", WORKFLOWS[0]["steps"][0]["data"])
    processor.run_step("create_order", {"items": [{"name": "Pen", "price": 1, "quantity": 1, "weight": 0.1}]})

    assert processor.run_step("set_shipping", {"distance_km": -1}) == {
        "status": "error",
        "error": "Distance cannot be negative",
    }


def test_gateway_normalizes_declined_card_numbers():
    gateway = SimulatedPaymentGateway(declined_cards=["4111-1111-1111-1111"])
    assert gateway.charge("4111 1111 1111 1111", 10)["approved"] is False
