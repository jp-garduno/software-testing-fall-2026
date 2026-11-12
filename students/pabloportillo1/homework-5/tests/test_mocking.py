import logging
from datetime import timedelta
from unittest.mock import Mock, call

import pytest
from doubles import OWNER_EMAIL, OWNER_PHONE

from notification_service import GatewayError, NotificationError
from task import Task, TaskPriority, TaskStatus
from task_repository import DatabaseError, RepositoryError, TaskFilter, TaskRepository
from task_service import DuplicateTitleError, TaskNotFoundError


class TestTaskServiceInteractions:
    def test_create_task_checks_title_then_saves_then_notifies(self, mocked_service, mock_repository, notifier):
        mock_repository.find_by_title.return_value = None
        recorder = Mock()
        recorder.attach_mock(mock_repository, "repository")
        recorder.attach_mock(notifier, "notifier")

        task = mocked_service.create_task("Write tests")

        assert recorder.mock_calls == [
            call.repository.find_by_title("Write tests"),
            call.repository.save(task),
            call.notifier.send_email(OWNER_EMAIL, "New Task Created", "Task 'Write tests' has been created"),
        ]

    def test_create_task_with_duplicate_title_does_not_save(self, mocked_service, mock_repository, notifier):
        mock_repository.find_by_title.return_value = Task("Write tests")

        with pytest.raises(DuplicateTitleError):
            mocked_service.create_task("Write tests")
        mock_repository.save.assert_not_called()
        notifier.send_email.assert_not_called()

    def test_update_task_status_saves_the_transitioned_task(self, mocked_service, mock_repository, make_task):
        task = make_task(TaskStatus.TODO)
        mock_repository.find_by_id.return_value = task

        mocked_service.update_task_status(7, TaskStatus.IN_PROGRESS)

        mock_repository.find_by_id.assert_called_once_with(7)
        mock_repository.save.assert_called_once_with(task)
        assert task.status == TaskStatus.IN_PROGRESS

    def test_update_status_of_missing_task_does_not_save(self, mocked_service, mock_repository, notifier):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(TaskNotFoundError):
            mocked_service.update_task_status(7, TaskStatus.DONE)
        mock_repository.save.assert_not_called()
        notifier.send_email.assert_not_called()

    def test_purge_task_deletes_through_repository(self, mocked_service, mock_repository):
        mock_repository.delete.return_value = True

        mocked_service.purge_task(7)

        mock_repository.delete.assert_called_once_with(7)

    def test_purge_unknown_task_raises_not_found(self, mocked_service, mock_repository):
        mock_repository.delete.return_value = False

        with pytest.raises(TaskNotFoundError, match="Task 7 not found"):
            mocked_service.purge_task(7)

    def test_search_tasks_without_filter_asks_repository_for_everything(self, mocked_service, mock_repository):
        mocked_service.search_tasks()

        mock_repository.search.assert_called_once_with(TaskFilter())

    def test_check_overdue_tasks_with_no_tasks_sends_nothing(self, mocked_service, mock_repository, notifier):
        mock_repository.find_all.return_value = []

        assert mocked_service.check_overdue_tasks() == []
        notifier.send_email.assert_not_called()


class TestErrorScenarios:
    def test_repository_failure_handled_gracefully(self, mocked_service, mock_repository, notifier):
        mock_repository.find_by_title.return_value = None
        mock_repository.save.side_effect = RepositoryError("Could not save task 'Write tests'")

        with pytest.raises(RepositoryError, match="Could not save task"):
            mocked_service.create_task("Write tests")
        notifier.send_email.assert_not_called()

    def test_repository_failure_on_lookup_stops_status_update(self, mocked_service, mock_repository, notifier):
        mock_repository.find_by_id.side_effect = RepositoryError("Could not load task 7")

        with pytest.raises(RepositoryError):
            mocked_service.update_task_status(7, TaskStatus.IN_PROGRESS)
        mock_repository.save.assert_not_called()
        notifier.send_email.assert_not_called()

    def test_notification_failure_does_not_break_workflow(self, mocked_service, mock_repository, notifier, caplog):
        mock_repository.find_by_title.return_value = None
        notifier.send_email.side_effect = NotificationError("SMTP server unavailable")

        with caplog.at_level(logging.WARNING, logger="task_service"):
            task = mocked_service.create_task("Write tests")

        assert task.title == "Write tests"
        mock_repository.save.assert_called_once_with(task)
        notifier.send_email.assert_called_once()
        assert "SMTP server unavailable" in caplog.text

    def test_email_failure_still_sends_sms_for_urgent_task(self, mocked_service, mock_repository, notifier):
        mock_repository.find_by_title.return_value = None
        notifier.send_email.side_effect = NotificationError("SMTP server unavailable")

        mocked_service.create_task("Fix production bug", priority=TaskPriority.URGENT)

        notifier.send_sms.assert_called_once_with(
            OWNER_PHONE, "New Task Created: Task 'Fix production bug' has been created"
        )

    def test_overdue_check_keeps_notifying_after_one_failure(self, clock, mocked_service, mock_repository, notifier):
        first = Task("Submit homework", due_date=clock.now + timedelta(hours=1))
        second = Task("Pay rent", due_date=clock.now + timedelta(hours=2))
        mock_repository.find_all.return_value = [first, second]
        notifier.send_email.side_effect = [NotificationError("timeout"), None]
        clock.advance(days=1)

        overdue = mocked_service.check_overdue_tasks()

        assert overdue == [first, second]
        assert notifier.send_email.call_count == 2


class TestTaskRepositoryWithMockedDatabase:
    def test_save_new_task_inserts_and_assigns_returned_id(self, mock_database):
        mock_database.insert.return_value = 42
        task = Task("Write tests")

        TaskRepository(mock_database).save(task)

        assert task.task_id == 42
        mock_database.update.assert_not_called()

    def test_save_existing_task_updates_instead_of_inserting(self, mock_database):
        task = Task("Write tests")
        task.task_id = 42

        TaskRepository(mock_database).save(task)

        mock_database.update.assert_called_once_with(42, task)
        mock_database.insert.assert_not_called()

    @pytest.mark.parametrize(
        "operation",
        [
            pytest.param(lambda repository: repository.save(Task("Write tests")), id="insert"),
            pytest.param(lambda repository: repository.find_by_id(1), id="get"),
            pytest.param(lambda repository: repository.find_all(), id="all"),
            pytest.param(lambda repository: repository.find_by_title("Write tests"), id="find-by-title"),
            pytest.param(lambda repository: repository.search(TaskFilter()), id="search"),
            pytest.param(lambda repository: repository.delete(1), id="delete"),
        ],
    )
    def test_database_failure_becomes_repository_error(self, mock_database, operation):
        outage = DatabaseError("connection lost")
        for method in (mock_database.insert, mock_database.get, mock_database.all, mock_database.delete):
            method.side_effect = outage

        with pytest.raises(RepositoryError) as raised:
            operation(TaskRepository(mock_database))
        assert raised.value.__cause__ is outage

    def test_database_failure_on_update_becomes_repository_error(self, mock_database):
        task = Task("Write tests")
        task.task_id = 42
        mock_database.update.side_effect = DatabaseError("deadlock")

        with pytest.raises(RepositoryError, match="Could not save task 'Write tests'"):
            TaskRepository(mock_database).save(task)

    def test_programming_errors_are_not_disguised_as_database_failures(self, mock_database):
        mock_database.get.side_effect = TypeError("unhashable type: 'list'")

        with pytest.raises(TypeError):
            TaskRepository(mock_database).find_by_id([1])

    def test_find_by_title_reads_the_database_through_a_spy(self, fake_database):
        spy = Mock(wraps=fake_database)
        repository = TaskRepository(spy)
        repository.save(Task("Write tests"))

        found = repository.find_by_title("write tests")

        assert found.title == "Write tests"
        spy.all.assert_called_once_with()


class TestNotificationServiceWithMockedGateways:
    def test_send_email_hands_message_to_gateway_once(self, notification_service, email_gateway):
        notification_service.send_email(OWNER_EMAIL, "Task Overdue", "Task 'Pay rent' is overdue")

        email_gateway.send.assert_called_once_with(OWNER_EMAIL, "Task Overdue", "Task 'Pay rent' is overdue")

    def test_send_sms_hands_message_to_gateway_once(self, notification_service, sms_gateway, email_gateway):
        notification_service.send_sms(OWNER_PHONE, "Task Overdue: Pay rent")

        sms_gateway.send.assert_called_once_with(OWNER_PHONE, "Task Overdue: Pay rent")
        email_gateway.send.assert_not_called()

    def test_transient_failure_is_retried_until_success(self, notification_service, email_gateway, caplog):
        email_gateway.send.side_effect = [GatewayError("timeout"), None]

        with caplog.at_level(logging.WARNING, logger="notification_service"):
            notification_service.send_email(OWNER_EMAIL, "Subject", "Body")

        assert email_gateway.send.call_count == 2
        assert "Email attempt 1 of 3 failed: timeout" in caplog.text

    def test_persistent_failure_raises_after_max_attempts(self, notification_service, sms_gateway):
        outage = GatewayError("provider down")
        sms_gateway.send.side_effect = outage

        with pytest.raises(NotificationError, match="SMS delivery failed after 3 attempts") as raised:
            notification_service.send_sms(OWNER_PHONE, "Task Overdue: Pay rent")
        assert sms_gateway.send.call_count == 3
        assert raised.value.__cause__ is outage

    def test_unexpected_error_is_not_retried(self, notification_service, email_gateway):
        email_gateway.send.side_effect = RuntimeError("bug in the client")

        with pytest.raises(RuntimeError, match="bug in the client"):
            notification_service.send_email(OWNER_EMAIL, "Subject", "Body")
        email_gateway.send.assert_called_once()

    def test_invalid_recipient_is_rejected_before_calling_gateway(self, notification_service, email_gateway):
        with pytest.raises(ValueError, match="Invalid email address"):
            notification_service.send_email("not-an-email", "Subject", "Body")
        email_gateway.send.assert_not_called()
