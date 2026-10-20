"""Shared, deterministic test data for TaskFlow."""

from datetime import datetime, timedelta

import pytest

from src.task import Task, TaskPriority


@pytest.fixture
def future_date() -> datetime:
    return datetime.now() + timedelta(days=7)


@pytest.fixture
def task(future_date: datetime) -> Task:
    return Task("Write tests", "A clear description", TaskPriority.HIGH, future_date)
