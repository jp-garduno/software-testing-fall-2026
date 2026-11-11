"""Part 4: end-to-end workflows from order_workflows.json, run against Checkout.

A workflow is a list of steps. Each step names a Checkout method ("action"),
gives its keyword arguments ("data") and lists the fields of the result that
must match ("expected").
"""

import pytest

from case_loaders import REFERENCE_DATE, load_workflows
from checkout import Checkout


@pytest.mark.parametrize("workflow", load_workflows("order_workflows.json"))
def test_order_workflow(workflow):
    """Run the steps in order on one checkout session; every expected field must match."""
    checkout = Checkout(today=REFERENCE_DATE)

    for number, step in enumerate(workflow["steps"], start=1):
        result = getattr(checkout, step["action"])(**step.get("data", {}))

        for field, expected in step["expected"].items():
            assert result[field] == expected, f"step {number} ({step['action']}): {field}"
