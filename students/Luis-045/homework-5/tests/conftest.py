"""Independent fixtures shared by the TaskFlow test suites."""

from datetime import datetime, timezone
from unittest.mock import Mock

import pytest


@pytest.fixture
def now():
    """Use a fixed instant so tests do not depend on the machine clock."""
    return datetime(2026, 10, 18, 12, tzinfo=timezone.utc)


@pytest.fixture
def clock(now):
    """Provide a callable clock whose return value a test can advance."""
    return Mock(return_value=now)
