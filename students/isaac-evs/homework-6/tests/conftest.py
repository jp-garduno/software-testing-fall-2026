from datetime import date, timedelta

import pytest


class FakeClock:
    """Controllable clock so date-dependent tests never use the real time."""

    def __init__(self, today=date(2026, 1, 1)):
        self.today = today

    def __call__(self):
        return self.today

    def advance(self, days):
        self.today += timedelta(days=days)


@pytest.fixture
def clock():
    return FakeClock()
