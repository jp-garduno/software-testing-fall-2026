"""EP: valid/invalid input partitions; IDs and expected values come from design."""
import pytest
from conftest import cases_for


@pytest.mark.parametrize("case", cases_for("EP"), ids=lambda case: f'{case["id"]}: {case["name"]}')
def test_equivalence_partition(case, run_case):
    """EP01 onward: exercise the documented representative of each partition."""
    run_case(case)
