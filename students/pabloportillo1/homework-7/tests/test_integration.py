import re

import pytest

from src.checkout import Checkout, CheckoutError
from tools.data_files import TEST_DATA_DIR, load_workflow_data

DATA = load_workflow_data(TEST_DATA_DIR / "order_workflows.json")


class FakeGateway:
    def __init__(self, available_credit):
        self.available_credit = available_credit
        self.charges = []

    def charge(self, card_number, amount):
        if amount > self.available_credit:
            return None
        self.available_credit -= amount
        self.charges.append((card_number, amount))
        return f"TXN-{len(self.charges):04d}"


def run_step(checkout, number, step):
    action = getattr(checkout, step["action"])
    data = step.get("data", {})
    if "expected_error" in step:
        with pytest.raises(CheckoutError, match=re.escape(step["expected_error"])):
            action(**data)
        return
    result = action(**data)
    actual = {key: result.get(key) for key in step["expected"]}
    assert actual == step["expected"], f"step {number}: {step['action']}"


@pytest.mark.parametrize("workflow", [pytest.param(flow, id=flow["name"]) for flow in DATA.workflows])
def test_workflow_each_step_returns_expected_result(workflow):
    checkout = Checkout(FakeGateway(workflow["gateway"]["available_credit"]), today=DATA.reference_date)

    for number, step in enumerate(workflow["steps"]):
        run_step(checkout, number, step)
