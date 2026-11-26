"""Regression tests over the 100 generated orders (bonus Option A)."""
import pytest

from data_loader import DATA_DIR, load_order_cases, run_order_case

pytestmark = pytest.mark.skipif(
    not (DATA_DIR / "generated_orders.csv").exists(),
    reason="run `python tools/generate_orders.py` first",
)


@pytest.mark.parametrize("case", load_order_cases("generated_orders.csv")
                         if (DATA_DIR / "generated_orders.csv").exists() else [])
def test_generated_order(case):
    run_order_case(case)
