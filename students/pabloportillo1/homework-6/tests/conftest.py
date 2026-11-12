from datetime import date, timedelta

import pytest


class FakeClock:
    def __init__(self, today):
        self.today = today

    def __call__(self):
        return self.today

    def advance(self, days):
        self.today += timedelta(days=days)


@pytest.fixture(name="clock")
def fixture_clock():
    return FakeClock(date(2026, 10, 1))
