"""End-to-end integration tests, driven by order_workflows.json.

Every workflow validates the customer, tries the discount, sets the shipping
and computes the total, then compares the whole outcome against the file.
"""

import pytest

from conftest import load_json
from customer_validator import validate_customer
from order_calculator import Order

WORKFLOWS = load_json("order_workflows.json")["workflows"]
ONE_CENT = 0.005


def run(workflow):
    """Run the whole workflow and return the observed outcome."""
    customer_valid, _ = validate_customer(workflow["customer"])
    order = Order(workflow["items"], workflow["customer_type"])

    discount_applied = False
    for step in workflow["steps"]:
        if step["action"] == "apply_discount":
            discount_applied = order.apply_discount(step["code"])
        elif step["action"] == "set_shipping":
            order.set_shipping(step["distance_km"], step["is_express"])

    return {
        "customer_valid": customer_valid,
        "discount_applied": discount_applied,
        "order": order.calculate_total(),
        "outcome": "confirmed" if customer_valid else "rejected_customer",
    }


@pytest.mark.parametrize("workflow", WORKFLOWS, ids=lambda workflow: workflow["workflow_name"])
def test_full_workflow(workflow):
    """Customer, discount, shipping and total of every workflow in the file."""
    result = run(workflow)

    assert result["customer_valid"] == workflow["expected_customer_valid"], workflow["description"]
    assert result["discount_applied"] == workflow["expected_discount_applied"], workflow["description"]
    assert result["outcome"] == workflow["expected_outcome"], workflow["description"]

    for key, expected in workflow["expected_order"].items():
        assert result["order"][key] == pytest.approx(expected, abs=ONE_CENT), f"{key} in {workflow['workflow_name']}"


class TestWorkflowCoverage:
    """The file has to cover more than the happy path."""

    def test_minimum_number_of_workflows(self):
        assert len(WORKFLOWS) >= 3

    def test_there_is_a_workflow_that_confirms(self):
        assert any(w["expected_outcome"] == "confirmed" for w in WORKFLOWS)

    def test_there_is_a_workflow_that_rejects_the_customer(self):
        assert any(w["expected_outcome"] == "rejected_customer" for w in WORKFLOWS)

    def test_there_is_a_workflow_where_the_discount_is_rejected(self):
        assert any(w["expected_discount_applied"] is False for w in WORKFLOWS)


def test_a_rejected_order_keeps_its_amounts():
    """A customer failing validation does not change the order amounts."""
    rejected = [w for w in WORKFLOWS if w["expected_outcome"] == "rejected_customer"]
    assert rejected, "a workflow with a rejected customer is needed"

    for workflow in rejected:
        result = run(workflow)
        assert result["order"]["total"] == pytest.approx(workflow["expected_order"]["total"], abs=ONE_CENT)
