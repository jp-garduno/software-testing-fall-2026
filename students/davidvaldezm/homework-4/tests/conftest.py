"""Fresh accounts and a deterministic clock for every black-box scenario."""

from datetime import datetime, timezone

import pytest

from banking_system import BankAccount


@pytest.fixture(name="clock")
def controlled_clock():
    """The mutable clock is an external dependency, not internal bank state."""

    class Clock:  # pylint: disable=too-few-public-methods
        """Callable time provider whose only behavior is returning current time."""

        now = datetime(2026, 9, 1, 12, tzinfo=timezone.utc)

        def __call__(self):
            return self.now

    return Clock()


@pytest.fixture
def account(clock):
    """Create independent accounts with an ample balance by default."""
    return lambda kind="Checking", balance="10000": BankAccount(kind, balance, clock)
