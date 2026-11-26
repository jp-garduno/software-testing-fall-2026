import csv

import pytest

from tests.order_cases import build_order, order_params
from tools import generate_orders
from tools.data_files import TEST_DATA_DIR, load_order_cases

SNAPSHOT = TEST_DATA_DIR / "generated_orders.csv"
CASES = load_order_cases(SNAPSHOT)


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


@pytest.mark.parametrize("case", order_params(CASES))
def test_calculate_total_generated_order_matches_snapshot(case):
    assert build_order(case).calculate_total() == case.expected


def test_main_same_seed_rewrites_identical_snapshot(tmp_path, monkeypatch):
    output = tmp_path / "test_data" / "generated_orders.csv"
    output.parent.mkdir()
    monkeypatch.setattr(generate_orders, "TEST_DATA_DIR", output.parent)
    monkeypatch.setattr(generate_orders, "OUTPUT", output)

    generate_orders.main()

    assert read_rows(output) == read_rows(SNAPSHOT)
