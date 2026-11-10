"""Part 4: Data-driven end-to-end integration tests using order_workflows.json."""

import json
from pathlib import Path
import pytest
from customer_validator import process_order_workflow

WORKFLOWS_PATH = Path(__file__).resolve().parent.parent / "test_data" / "order_workflows.json"


def load_workflows():
    """Load end-to-end workflows from JSON."""
    data = json.loads(WORKFLOWS_PATH.read_text(encoding="utf-8"))
    return data["workflows"]


WORKFLOWS = load_workflows()


@pytest.mark.parametrize("workflow", WORKFLOWS, ids=[w["name"] for w in WORKFLOWS])
def test_end_to_end_order_workflow(workflow):
    """Execute each workflow step-by-step and verify expected outcomes."""
    state = process_order_workflow(workflow)
    steps = workflow["steps"]

    assert len(state["step_results"]) == len(steps)

    for step_spec, actual_step in zip(steps, state["step_results"]):
        action = step_spec["action"]
        expected = step_spec["expected"]

        if action == "validate_customer":
            assert actual_step["valid"] is expected["valid"]
        elif action == "create_order":
            assert actual_step["status"] == expected["status"]
        elif action == "calculate_total":
            for key, exp_val in expected.items():
                assert actual_step[key] == pytest.approx(exp_val, abs=1e-2)
        elif action == "process_payment":
            assert actual_step["status"] == expected["status"]


def test_workflow_calculate_total_without_order():
    """Verify workflow handles calculate_total and process_payment when no order was created."""
    workflow = {
        "name": "missing_order_step",
        "steps": [
            {"action": "calculate_total", "expected": {}},
            {"action": "process_payment", "expected": {"status": "failed"}},
        ],
    }
    state = process_order_workflow(workflow)
    assert state["step_results"][0]["error"] == "No active order"
    assert state["payment_status"] == "failed"
