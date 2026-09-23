"""DT: every rule in the transfer, fee, and bill decision tables."""
import pytest
from conftest import cases_for


@pytest.mark.parametrize("case", cases_for("DT"), ids=lambda case: f'{case["id"]}: {case["name"]}')
def test_decision_rule(case, run_case):
    """DT01 onward: test combinations, precedence, and fee-processing guards."""
    run_case(case)
