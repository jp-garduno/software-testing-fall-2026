"""Pytest hooks: validate every test data file before any test is collected (bonus option C)."""

import pytest
from src.data_validator import format_report, validate_all
from tests.data_loader import TEST_DATA_DIR


def pytest_sessionstart() -> None:
    """Abort the run with a 'file:line: message' report when a data file is malformed."""
    issues = validate_all(TEST_DATA_DIR)
    if issues:
        raise pytest.UsageError(format_report(issues))
