import pytest

from src.customer_validator import validate_customer
from tools.data_files import TEST_DATA_DIR, load_customer_data

DATA = load_customer_data(TEST_DATA_DIR / "customer_validation.json")


@pytest.mark.parametrize("case", [pytest.param(case, id=case.test_name) for case in DATA.cases])
def test_validate_customer_returns_expected_errors(case):
    result = validate_customer(case.customer, today=DATA.reference_date)

    assert (result.is_valid, list(result.errors)) == (case.is_valid, case.errors)
