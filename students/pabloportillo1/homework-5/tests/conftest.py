from unittest.mock import create_autospec, patch

import pytest
from doubles import OWNER_EMAIL, OWNER_PHONE, FakeDatabase, FrozenClock

from notification_service import EmailGateway, NotificationService, SmsGateway
from task import Task, TaskStatus
from task_repository import Database, TaskRepository
from task_service import TaskService

LIFECYCLE_PATHS = {
    TaskStatus.TODO: (),
    TaskStatus.IN_PROGRESS: (TaskStatus.IN_PROGRESS,),
    TaskStatus.DONE: (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    TaskStatus.ARCHIVED: (TaskStatus.ARCHIVED,),
}


@pytest.fixture(name="clock")
def fixture_clock():
    with patch("task.datetime") as patched_datetime:
        yield FrozenClock(patched_datetime)


@pytest.fixture(name="make_task")
def fixture_make_task():
    """Build a task and walk it through the lifecycle to the requested status."""

    def _make(status=TaskStatus.TODO, title="Write unit tests", **fields):
        task = Task(title, **fields)
        for step in LIFECYCLE_PATHS[status]:
            task.transition_to(step)
        return task

    return _make


@pytest.fixture(name="fake_database")
def fixture_fake_database():
    return FakeDatabase()


@pytest.fixture(name="repository")
def fixture_repository(fake_database):
    return TaskRepository(fake_database)


@pytest.fixture(name="notifier")
def fixture_notifier():
    return create_autospec(NotificationService, instance=True)


@pytest.fixture(name="service")
def fixture_service(repository, notifier):
    """TaskService over the real repository and an in-memory database, with notifications mocked."""
    return TaskService(repository, notifier, OWNER_EMAIL, OWNER_PHONE)


@pytest.fixture(name="mock_repository")
def fixture_mock_repository():
    return create_autospec(TaskRepository, instance=True)


@pytest.fixture(name="mocked_service")
def fixture_mocked_service(mock_repository, notifier):
    """TaskService with both the repository and the notification service replaced by mocks."""
    return TaskService(mock_repository, notifier, OWNER_EMAIL, OWNER_PHONE)


@pytest.fixture(name="mock_database")
def fixture_mock_database():
    return create_autospec(Database, instance=True)


@pytest.fixture(name="email_gateway")
def fixture_email_gateway():
    return create_autospec(EmailGateway, instance=True)


@pytest.fixture(name="sms_gateway")
def fixture_sms_gateway():
    return create_autospec(SmsGateway, instance=True)


@pytest.fixture(name="notification_service")
def fixture_notification_service(email_gateway, sms_gateway):
    return NotificationService(email_gateway, sms_gateway)
