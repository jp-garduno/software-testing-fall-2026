"""TaskService integration tests with repository and notification boundaries mocked."""

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from src.notification_service import NotificationService
from src.task import Task, TaskPriority, TaskStatus
from src.task_repository import TaskRepository
from src.task_service import TaskService


@pytest.fixture
def repository():
    return Mock(spec=TaskRepository)


@pytest.fixture
def notifications():
    return Mock(spec=NotificationService)


@pytest.fixture
def service(repository, notifications):
    return TaskService(repository, notifications)


class TestCreation:
    def test_creates_saves_and_notifies(self, service, repository, notifications):
        repository.find_by_title.return_value = None

        task = service.create_task("Write tests", priority=TaskPriority.HIGH)

        assert task.status is TaskStatus.TODO
        repository.save.assert_called_once_with(task)
        notifications.send_email.assert_called_once_with(
            "user@example.com",
            "New Task Created",
            "Task 'Write tests' has been created.",
        )

    def test_rejects_duplicate_title_without_side_effects(
        self, service, repository, notifications
    ):
        repository.find_by_title.return_value = Task("Existing task")

        with pytest.raises(ValueError, match="already exists"):
            service.create_task("Existing task")

        repository.save.assert_not_called()
        notifications.send_email.assert_not_called()

    def test_urgent_task_uses_email_and_sms(self, service, repository, notifications):
        repository.find_by_title.return_value = None

        task = service.create_task("Incident response", priority=TaskPriority.URGENT)

        repository.save.assert_called_once_with(task)
        notifications.send_sms.assert_called_once_with(
            "+15555550100", "Urgent task: Incident response"
        )

    def test_notification_failure_does_not_undo_saved_task(
        self, service, repository, notifications
    ):
        repository.find_by_title.return_value = None
        notifications.send_email.side_effect = RuntimeError("SMTP unavailable")

        task = service.create_task("Resilient task")

        assert task.title == "Resilient task"
        repository.save.assert_called_once_with(task)
        notifications.send_email.assert_called_once()

    def test_repository_failure_prevents_notification(
        self, service, repository, notifications
    ):
        repository.find_by_title.return_value = None
        repository.save.side_effect = RuntimeError("Database unavailable")

        with pytest.raises(RuntimeError, match="Database unavailable"):
            service.create_task("Database task")

        notifications.send_email.assert_not_called()


class TestStatusWorkflow:
    def test_complete_workflow_from_todo_to_done(
        self, service, repository, notifications
    ):
        task = Task("Workflow task")
        repository.find_by_id.return_value = task

        service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        completed = service.update_task_status(task.id, TaskStatus.DONE)

        assert completed.status is TaskStatus.DONE
        assert repository.save.call_count == 2
        assert notifications.send_email.call_count == 2
        assert "IN_PROGRESS to DONE" in notifications.send_email.call_args.args[2]

    def test_status_change_notifies_after_persisting(
        self, service, repository, notifications
    ):
        task = Task("Ordered calls")
        repository.find_by_id.return_value = task
        events = []
        repository.save.side_effect = lambda saved: events.append(
            ("save", saved.status)
        )
        notifications.send_email.side_effect = lambda *_: events.append(
            ("email", task.status)
        )

        service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        assert events == [
            ("save", TaskStatus.IN_PROGRESS),
            ("email", TaskStatus.IN_PROGRESS),
        ]

    def test_rejects_status_change_for_missing_task(
        self, service, repository, notifications
    ):
        repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            service.update_task_status(99, TaskStatus.DONE)

        repository.save.assert_not_called()
        notifications.send_email.assert_not_called()

    def test_rejects_invalid_status_change_without_side_effects(
        self, service, repository, notifications
    ):
        task = Task("Completed task")
        task.status = TaskStatus.DONE
        repository.find_by_id.return_value = task

        with pytest.raises(ValueError, match="Invalid transition"):
            service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        repository.save.assert_not_called()
        notifications.send_email.assert_not_called()

    def test_archiving_is_idempotent(self, service, repository, notifications):
        task = Task("Archive task")
        task.status = TaskStatus.ARCHIVED
        repository.find_by_id.return_value = task

        assert service.archive_task(task.id) is task

        repository.save.assert_not_called()
        notifications.send_email.assert_not_called()

    def test_archiving_active_task_persists_and_notifies(
        self, service, repository, notifications
    ):
        task = Task("Archive me")
        repository.find_by_id.return_value = task

        archived = service.archive_task(task.id)

        assert archived.status is TaskStatus.ARCHIVED
        repository.save.assert_called_once_with(task)
        assert "TODO to ARCHIVED" in notifications.send_email.call_args.args[2]


class TestUpdatesAndSearching:
    def test_updates_fields_after_excluding_same_task_from_duplicate_check(
        self, service, repository, notifications
    ):
        task = Task("Original task")
        repository.find_by_id.return_value = task
        repository.find_by_title.return_value = task

        updated = service.update_task(
            task.id, title="Original task", priority=TaskPriority.HIGH
        )

        assert updated.priority is TaskPriority.HIGH
        repository.save.assert_called_once_with(task)
        notifications.send_email.assert_not_called()

    def test_rejects_duplicate_title_on_update(self, service, repository):
        task = Task("Original task")
        repository.find_by_id.return_value = task
        repository.find_by_title.return_value = Task("Another task")

        with pytest.raises(ValueError, match="already exists"):
            service.update_task(task.id, title="Another task")

        repository.save.assert_not_called()

    def test_overdue_check_notifies_only_matching_tasks(
        self, service, repository, notifications
    ):
        now = datetime(2030, 1, 10)
        overdue = Task("Late task")
        overdue.due_date = now - timedelta(days=1)
        future = Task("Future task", due_date=now + timedelta(days=1))
        done = Task("Done task")
        done.due_date = now - timedelta(days=1)
        done.status = TaskStatus.DONE
        repository.find_all.return_value = [overdue, future, done]

        found = service.check_overdue_tasks(now)

        assert found == [overdue]
        notifications.send_email.assert_called_once_with(
            "user@example.com", "Task Overdue", "Task 'Late task' is overdue."
        )

    def test_search_combines_status_priority_title_and_date_filters(
        self, service, repository
    ):
        start = datetime(2030, 1, 1)
        matching = Task(
            "Deploy API", priority=TaskPriority.HIGH, due_date=start + timedelta(days=2)
        )
        matching.status = TaskStatus.IN_PROGRESS
        wrong_priority = Task("Deploy docs", due_date=start + timedelta(days=2))
        wrong_priority.status = TaskStatus.IN_PROGRESS
        wrong_title = Task(
            "Review API", priority=TaskPriority.HIGH, due_date=start + timedelta(days=2)
        )
        wrong_title.status = TaskStatus.IN_PROGRESS
        repository.find_all.return_value = [matching, wrong_priority, wrong_title]

        found = service.search_tasks(
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            title_contains="DEPLOY",
            due_between=(start, start + timedelta(days=3)),
        )

        assert found == [matching]

    def test_search_without_filters_returns_all_tasks(self, service, repository):
        tasks = [Task("First task"), Task("Second task")]
        repository.find_all.return_value = tasks

        assert service.search_tasks() == tasks
