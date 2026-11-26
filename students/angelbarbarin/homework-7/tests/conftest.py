"""Shared paths and the data-file check that runs before any test (bonus option C)."""

from datetime import date
from pathlib import Path

import pytest

from data_files import validate_directory

# Paths are resolved from this file, so the suite works from any working directory.
HOMEWORK_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = HOMEWORK_DIR / "test_data"

# Card expirations in the JSON files are judged against this date, so results never
# change with the day the suite runs. A case can override it with its own "today".
REFERENCE_DATE = date(2026, 11, 1)


@pytest.fixture(name="reference_date")
def fixture_reference_date():
    return REFERENCE_DATE


def pytest_sessionstart(session):  # pylint: disable=unused-argument
    """Refuse to run the suite on broken data and list every problem with its line number."""
    errors = validate_directory(DATA_DIR)
    if errors:
        details = "\n".join(f"  {error}" for error in errors)
        raise pytest.UsageError(f"Invalid test data ({len(errors)} problem(s)):\n{details}")
