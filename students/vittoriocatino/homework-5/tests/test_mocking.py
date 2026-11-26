"""Tests demonstrating mock boundaries and abstract-adapter behavior."""

import pytest

from notification_service import NotificationService
from task import Task
from task_repository import TaskRepository


@pytest.mark.parametrize(
    "method,args",
    [
        ("save", (Task("Saved task"),)),
        ("find_by_id", (1,)),
        ("find_by_title", ("Title",)),
        ("find_all", ()),
        ("delete", (1,)),
    ],
)
def test_repository_boundary_requires_a_concrete_adapter(method, args):
    """The repository interface makes real persistence an explicit test boundary."""
    with pytest.raises(NotImplementedError, match="persistence adapter"):
        getattr(TaskRepository(), method)(*args)


@pytest.mark.parametrize(
    "method,args",
    [
        ("send_email", ("a@b.com", "Subject", "Body")),
        ("send_sms", ("+15550000000", "Message")),
    ],
)
def test_notification_boundary_requires_a_concrete_adapter(method, args):
    """The notification interface prevents accidental real external calls in tests."""
    with pytest.raises(NotImplementedError, match="notification adapter"):
        getattr(NotificationService(), method)(*args)
