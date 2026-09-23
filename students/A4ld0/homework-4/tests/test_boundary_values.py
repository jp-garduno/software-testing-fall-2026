"""BV: exact monetary, calendar, and cumulative allowance boundaries."""
import pytest
from conftest import cases_for


@pytest.mark.parametrize("case", cases_for("BV"), ids=lambda case: f'{case["id"]}: {case["name"]}')
def test_boundary_value(case, run_case):
    """BV01 onward: check on/below/above boundaries against independent oracles."""
    run_case(case)
