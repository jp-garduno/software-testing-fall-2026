"""Integration tests: TaskService together with the repository and the Task model.

Tests that use fake_service run the real TaskRepository over an in-memory database, so service,
repository and model really work together. The rest mock the repository to pin down exactly which
calls the service makes. The notifier is an external dependency and is always mocked.
"""

import pytest

from task import Task, TaskPriority, TaskStateError, TaskStatus
from task_service import DuplicateTitleError, TaskNotFoundError

EMAIL = "user@example.com"


def stored_task(task_id, title="Existing task", status=TaskStatus.TODO):
    """A task as the repository would return it: already saved, with an id."""
    task = Task(title)
    task.id = task_id
    task.status = status
    return task


class TestTaskCreation:
    def test_create_task_success_with_notification(self, service, mock_repository, mock_notifier):
        task = service.create_task("Write tests", "Unit and integration tests", TaskPriority.HIGH)

        assert task.title == "Write tests"
        assert task.status is TaskStatus.TODO
        mock_repository.find_by_title.assert_called_once_with("Write tests")
        mock_repository.save.assert_called_once_with(task)
        mock_notifier.send_email.assert_called_once_with(
            EMAIL, "New Task Created", "Task 'Write tests' has been created"
        )
        mock_notifier.send_sms.assert_not_called()

    def test_create_task_with_duplicate_title_fails(self, service, mock_repository, mock_notifier):
        mock_repository.find_by_title.return_value = stored_task(1, "Existing Task")

        with pytest.raises(DuplicateTitleError, match="already exists"):
            service.create_task("Existing Task")

        mock_repository.save.assert_not_called()
        mock_notifier.send_email.assert_not_called()

    def test_create_task_with_invalid_title_never_reaches_repository(self, service, mock_repository):
        with pytest.raises(ValueError, match="at least 3 characters"):
            service.create_task("ab")

        mock_repository.find_by_title.assert_not_called()
        mock_repository.save.assert_not_called()

    def test_create_urgent_task_also_sends_sms(self, service, mock_notifier):
        service.create_task("Server down", priority=TaskPriority.URGENT)

        mock_notifier.send_email.assert_called_once()
        mock_notifier.send_sms.assert_called_once_with(
            service.recipient_phone, "New Task Created: Task 'Server down' has been created"
        )


class TestStatusManagement:
    def test_update_task_status_triggers_notification(self, service, mock_repository, mock_notifier):
        task = stored_task(1)
        mock_repository.find_by_id.return_value = task

        updated = service.update_task_status(1, TaskStatus.IN_PROGRESS)

        assert updated.status is TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once_with(task)
        subject, body = mock_notifier.send_email.call_args.args[1:]
        assert subject == "Task Status Updated"
        assert "from TODO to IN_PROGRESS" in body

    def test_update_task_with_invalid_transition_fails(self, service, mock_repository, mock_notifier):
        mock_repository.find_by_id.return_value = stored_task(1, status=TaskStatus.DONE)

        with pytest.raises(TaskStateError, match="Invalid transition"):
            service.update_task_status(1, TaskStatus.IN_PROGRESS)

        mock_repository.save.assert_not_called()
        mock_notifier.send_email.assert_not_called()

    def test_update_status_of_missing_task_fails(self, service, mock_repository, mock_notifier):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(TaskNotFoundError, match="Task 99 not found"):
            service.update_task_status(99, TaskStatus.DONE)

        mock_notifier.send_email.assert_not_called()

    def test_delete_task_marks_as_archived(self, service, mock_repository, mock_notifier):
        task = stored_task(1)
        mock_repository.find_by_id.return_value = task

        service.delete_task(1)

        assert task.status is TaskStatus.ARCHIVED
        mock_repository.save.assert_called_once_with(task)
        mock_repository.delete.assert_not_called()
        assert "from TODO to ARCHIVED" in mock_notifier.send_email.call_args.args[2]

    def test_complete_workflow_todo_to_done(self, fake_service, mock_notifier):
        task = fake_service.create_task("Complete workflow task")
        fake_service.update_task(task.id, description="Now with a description")
        fake_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        fake_service.update_task_status(task.id, TaskStatus.DONE)

        stored = fake_service.get_task(task.id)
        assert stored.status is TaskStatus.DONE
        assert stored.description == "Now with a description"
        subjects = [sent.args[1] for sent in mock_notifier.send_email.call_args_list]
        assert subjects == ["New Task Created", "Task Status Updated", "Task Status Updated"]

    def test_archive_task_prevents_further_updates(self, fake_service):
        task = fake_service.create_task("Old project")
        fake_service.delete_task(task.id)

        with pytest.raises(TaskStateError, match="cannot be modified"):
            fake_service.update_task(task.id, title="Revived project")
        with pytest.raises(TaskStateError, match="Invalid transition from ARCHIVED"):
            fake_service.update_task_status(task.id, TaskStatus.TODO)
        assert fake_service.get_task(task.id).title == "Old project"

    def test_purged_task_cannot_be_recovered(self, fake_service):
        task = fake_service.create_task("Temporary task")
        fake_service.delete_task(task.id)

        fake_service.purge_task(task.id)

        with pytest.raises(TaskNotFoundError):
            fake_service.get_task(task.id)


class TestUpdatesAndOverdue:
    def test_update_task_with_duplicate_title_fails(self, service, mock_repository):
        mock_repository.find_by_id.return_value = stored_task(1, "Write report")
        mock_repository.find_by_title.return_value = stored_task(2, "Review report")

        with pytest.raises(DuplicateTitleError):
            service.update_task(1, title="Review report")

        mock_repository.save.assert_not_called()

    def test_overdue_task_detection_triggers_notification(self, service, mock_repository, mock_notifier, clock):
        overdue = Task("Overdue task", due_date=clock.in_days(1))
        future = Task("Future task", due_date=clock.in_days(5))
        finished = Task("Finished task", due_date=clock.in_days(1))
        finished.status = TaskStatus.DONE
        mock_repository.find_all.return_value = [overdue, future, finished]
        clock.advance(days=2)

        result = service.check_overdue_tasks()

        assert result == [overdue]
        mock_notifier.send_email.assert_called_once_with(EMAIL, "Task Overdue", "Task 'Overdue task' is overdue!")


class TestSearchAndFilter:
    @pytest.fixture(name="seeded_service")
    def fixture_seeded_service(self, fake_service, clock):
        fake_service.create_task("Write unit tests", priority=TaskPriority.HIGH, due_date=clock.in_days(2))
        fake_service.create_task("Write integration tests", priority=TaskPriority.HIGH, due_date=clock.in_days(10))
        fake_service.create_task("Plan sprint", priority=TaskPriority.LOW)
        fake_service.create_task("Fix login outage", priority=TaskPriority.URGENT, due_date=clock.in_days(1))
        fake_service.update_task_status(1, TaskStatus.IN_PROGRESS)
        return fake_service

    @staticmethod
    def titles(tasks):
        return [task.title for task in tasks]

    def test_search_tasks_by_status(self, seeded_service):
        assert self.titles(seeded_service.search_tasks(status=TaskStatus.IN_PROGRESS)) == ["Write unit tests"]

    def test_filter_tasks_by_priority(self, seeded_service):
        found = seeded_service.search_tasks(priority=TaskPriority.HIGH)
        assert self.titles(found) == ["Write unit tests", "Write integration tests"]

    def test_search_tasks_by_partial_title(self, seeded_service):
        assert self.titles(seeded_service.search_tasks(title_contains="TESTS")) == [
            "Write unit tests",
            "Write integration tests",
        ]

    def test_search_combines_multiple_filters(self, seeded_service, clock):
        found = seeded_service.search_tasks(
            status=TaskStatus.TODO, priority=TaskPriority.HIGH, title_contains="write", due_to=clock.in_days(14)
        )
        assert self.titles(found) == ["Write integration tests"]

    def test_filter_tasks_by_date_range(self, seeded_service, clock):
        found = seeded_service.search_tasks(due_from=clock.now, due_to=clock.in_days(3))
        assert self.titles(found) == ["Write unit tests", "Fix login outage"]

    def test_list_by_priority_puts_urgent_first(self, seeded_service):
        assert self.titles(seeded_service.list_by_priority()) == [
            "Fix login outage",
            "Write unit tests",
            "Write integration tests",
            "Plan sprint",
        ]
