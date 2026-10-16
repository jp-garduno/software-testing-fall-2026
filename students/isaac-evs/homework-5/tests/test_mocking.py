"""Mocking and isolation: mocks, stubs and fakes, error scenarios, and interaction checks.

Test double used in each class:
  * Mock  - verifies behaviour (was it called, with what, how often, in which order)
  * Stub  - returns canned answers (return_value / side_effect) so the code under test can run
  * Fake  - a simplified working implementation (FakeDatabase from conftest.py)
"""

from unittest.mock import ANY, Mock, call

import pytest

from notification_service import NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import RepositoryError, TaskRepository
from task_service import TaskService


class TestMocksVerifyBehaviour:
    def test_save_is_called_exactly_once_with_the_created_task(self, task_service, mock_repository):
        mock_repository.find_by_title.return_value = None

        task = task_service.create_task("Verify save")

        mock_repository.save.assert_called_once_with(task)

    def test_email_arguments_are_verified_with_any_for_free_text(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None

        task_service.create_task("Verify email")

        mock_notification_service.send_email.assert_called_once_with("user@example.com", "New Task Created", ANY)

    def test_configured_recipient_is_used_for_notifications(self, mock_repository, mock_notification_service, now):
        mock_repository.find_by_title.return_value = None
        service = TaskService(mock_repository, mock_notification_service, clock=lambda: now, recipient="boss@corp.test")

        service.create_task("Custom recipient")

        assert mock_notification_service.send_email.call_args[0][0] == "boss@corp.test"

    def test_save_happens_before_the_notification(self, mock_repository, mock_notification_service, now):
        mock_repository.find_by_title.return_value = None
        order = Mock()
        order.attach_mock(mock_repository.save, "save")
        order.attach_mock(mock_notification_service.send_email, "send_email")
        service = TaskService(mock_repository, mock_notification_service, clock=lambda: now)

        service.create_task("Ordering matters")

        assert [c[0] for c in order.mock_calls] == ["save", "send_email"]

    def test_call_count_matches_number_of_overdue_tasks(
        self, task_service, mock_repository, mock_notification_service, past, now
    ):
        late = []
        for name in ("Late one", "Late two"):
            task = Task(name, now=now)
            task.due_date = past
            late.append(task)
        mock_repository.find_all.return_value = late

        task_service.check_overdue_tasks()

        assert mock_notification_service.send_email.call_count == 2
        mock_notification_service.send_email.assert_has_calls(
            [
                call("user@example.com", "Task Overdue", "Task 'Late one' is overdue!"),
                call("user@example.com", "Task Overdue", "Task 'Late two' is overdue!"),
            ]
        )

    def test_mock_with_spec_rejects_methods_the_real_class_does_not_have(self, mock_notification_service):
        with pytest.raises(AttributeError):
            mock_notification_service.send_pigeon("hello")


class TestStubsProvideData:
    def test_stubbed_lookup_returns_the_prepared_task(self, task_service, mock_repository):
        prepared = Task("Prepared task")
        mock_repository.find_by_id.return_value = prepared

        assert task_service.get_task(42) is prepared
        mock_repository.find_by_id.assert_called_once_with(42)

    def test_stub_can_return_different_answers_per_call(self, task_service, mock_repository):
        first, second = Task("First task"), Task("Second task")
        mock_repository.find_by_id.side_effect = [first, second, None]

        assert task_service.get_task(1) is first
        assert task_service.get_task(2) is second
        with pytest.raises(ValueError, match="not found"):
            task_service.get_task(3)

    def test_stubbed_search_results_are_sorted_by_the_service(self, task_service, mock_repository):
        low = Task("Low task", priority=TaskPriority.LOW)
        urgent = Task("Urgent task", priority=TaskPriority.URGENT)
        mock_repository.search.return_value = [low, urgent]

        assert task_service.search_tasks() == [urgent, low]


class TestFakeKeepsState:
    def test_fake_database_round_trips_a_task_through_the_real_repository(self, fake_database):
        repository = TaskRepository(fake_database)
        task = repository.save(Task("Round trip"))

        assert task.id == 1
        assert repository.find_by_id(1) is task
        assert repository.delete(1) is True
        assert repository.find_by_id(1) is None

    def test_fake_assigns_distinct_ids(self, fake_service):
        service, _, _ = fake_service

        ids = {service.create_task(f"Task number {n}").id for n in range(5)}

        assert ids == {1, 2, 3, 4, 5}

    def test_tests_do_not_share_state_between_runs(self, fake_database):
        assert fake_database.all() == []


class TestRepositoryFailures:
    def test_repository_failure_on_create_is_propagated_and_not_notified(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None
        mock_repository.save.side_effect = RepositoryError("Database connection failed")

        with pytest.raises(RepositoryError, match="Database connection failed"):
            task_service.create_task("Doomed task")

        mock_notification_service.send_email.assert_not_called()

    def test_repository_failure_on_status_update_leaves_no_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_id.return_value = Task("Status task")
        mock_repository.save.side_effect = RepositoryError("disk full")

        with pytest.raises(RepositoryError):
            task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        mock_notification_service.send_email.assert_not_called()

    def test_repository_failure_during_lookup_is_propagated(self, task_service, mock_repository):
        mock_repository.find_by_title.side_effect = RepositoryError("timeout")

        with pytest.raises(RepositoryError, match="timeout"):
            task_service.create_task("Lookup fails")

    def test_database_errors_are_wrapped_in_repository_error(self):
        broken_database = Mock()
        broken_database.save.side_effect = ConnectionError("db down")
        repository = TaskRepository(broken_database)

        with pytest.raises(RepositoryError, match="db down") as excinfo:
            repository.save(Task("Wrapped error"))

        assert isinstance(excinfo.value.__cause__, ConnectionError)


class TestNotificationFailures:
    def test_notification_failure_does_not_prevent_task_creation(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None
        mock_notification_service.send_email.side_effect = Exception("SMTP server unavailable")

        task = task_service.create_task("Survives SMTP outage")

        assert task.title == "Survives SMTP outage"
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()

    def test_notification_failure_does_not_roll_back_a_status_change(
        self, task_service, mock_repository, mock_notification_service
    ):
        task = Task("Status survives")
        mock_repository.find_by_id.return_value = task
        mock_notification_service.send_email.side_effect = Exception("SMTP server unavailable")

        task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        assert task.status == TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once_with(task)

    def test_notification_failure_does_not_stop_the_overdue_sweep(
        self, task_service, mock_repository, mock_notification_service, past, now
    ):
        tasks = []
        for name in ("Late one", "Late two"):
            task = Task(name, now=now)
            task.due_date = past
            tasks.append(task)
        mock_repository.find_all.return_value = tasks
        mock_notification_service.send_email.side_effect = Exception("down")

        assert task_service.check_overdue_tasks() == tasks
        assert mock_notification_service.send_email.call_count == 2

    def test_sms_failure_does_not_break_urgent_task_creation(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None
        mock_notification_service.send_sms.side_effect = Exception("SMS gateway down")

        task = task_service.create_task_with_sms("Urgent despite SMS", priority=TaskPriority.URGENT)

        assert task.priority == TaskPriority.URGENT
        mock_notification_service.send_email.assert_called_once()
        mock_notification_service.send_sms.assert_called_once_with("+15555550100", ANY)

    def test_multiple_notification_channels_for_urgent_tasks(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None

        task_service.create_task_with_sms("Urgent task", priority=TaskPriority.URGENT)

        assert mock_notification_service.send_email.called
        assert mock_notification_service.send_sms.called


class TestGatewayWithMockedTransports:
    """NotificationService itself is the boundary: its transports are what get mocked."""

    def test_email_is_delegated_to_the_email_client(self):
        email_client = Mock()
        service = NotificationService(email_client=email_client)

        service.send_email("a@b.test", "Hi", "Body")

        email_client.send.assert_called_once_with("a@b.test", "Hi", "Body")

    def test_sms_is_delegated_to_the_sms_client(self):
        sms_client = Mock()
        service = NotificationService(sms_client=sms_client)

        service.send_sms("+15550001", "Hello")

        sms_client.send.assert_called_once_with("+15550001", "Hello")

    def test_client_failure_is_reported_as_notification_error(self):
        from notification_service import NotificationError

        email_client = Mock()
        email_client.send.side_effect = TimeoutError("slow")
        service = NotificationService(email_client=email_client)

        with pytest.raises(NotificationError, match="slow"):
            service.send_email("a@b.test", "Hi", "Body")
