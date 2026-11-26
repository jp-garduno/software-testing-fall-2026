"""Part 4: Data-driven end-to-end integration workflow tests."""

import json
from pathlib import Path

import pytest

from src.order_workflow import OrderWorkflowEngine

BASE_DIR = Path(__file__).resolve().parent.parent
WORKFLOWS_PATH = BASE_DIR / "test_data" / "order_workflows.json"


def load_workflows():
    """Load end-to-end order workflows from JSON."""
    with WORKFLOWS_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return [(wf["name"], wf["steps"]) for wf in payload["workflows"]]


@pytest.mark.parametrize(
    "workflow_name,steps",
    load_workflows(),
    ids=lambda val: val if isinstance(val, str) else "",
)
def test_end_to_end_order_workflows(workflow_name, steps):
    """Execute each multi-step workflow and assert expected step outputs."""
    engine = OrderWorkflowEngine()
    outputs = engine.run_workflow(steps)

    for step, actual in zip(steps, outputs):
        expected = step["expected"]
        for key, exp_val in expected.items():
            if isinstance(exp_val, float):
                assert actual[key] == pytest.approx(
                    exp_val, abs=1e-2
                ), f"{workflow_name} ({step['action']}): {key} mismatch"
            else:
                assert (
                    actual[key] == exp_val
                ), f"{workflow_name} ({step['action']}): {key} mismatch"


def test_workflow_engine_edge_cases():
    """Verify workflow engine handles uncreated orders, zero-total orders, and unknown actions."""
    engine = OrderWorkflowEngine()
    calc_before_create = engine.execute_step({"action": "calculate_total"})
    assert calc_before_create["total"] == 0.0

    engine.execute_step(
        {
            "action": "validate_customer",
            "data": {
                "email": "john@example.com",
                "phone": "(555) 123-4567",
                "billing_address": {
                    "street": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "zip": "10001",
                },
                "credit_card": {
                    "number": "4532015112830366",
                    "expiration": "12/2027",
                    "cvv": "123",
                },
            },
        }
    )
    engine.execute_step({"action": "create_order", "data": {"items": []}})
    payment_res = engine.execute_step({"action": "process_payment"})
    assert payment_res["status"] == "failed"

    with pytest.raises(ValueError, match="Unsupported workflow action"):
        engine.execute_step({"action": "unknown_action"})
