"""ST: valid transitions, invalid transitions, and terminal Closed behavior."""
import pytest
from conftest import cases_for


@pytest.mark.parametrize("case", cases_for("ST"), ids=lambda case: f'{case["id"]}: {case["name"]}')
def test_state_transition(case, run_case):
    """ST01 onward: reach states with public actions and assert sequence checkpoints."""
    run_case(case)
