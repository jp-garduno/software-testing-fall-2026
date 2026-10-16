"""Integration tests: TaskService working with its collaborators.

The notification service is always mocked. Tests that need real state use a real
TaskRepository over an in-memory fake database; the rest stub the repository.
"""

from datetime import timedelta

import pytest

from task import Task, TaskPriority, TaskStatus
from task_service import TaskService


class TestCreateTask:
    def test_create_task_success_with_notification(self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None

        task = task_service.create_task("Write tests", "Unit and integration", TaskPriority.HIGH)

        assert task.title == "Write tests"
        assert task.status == TaskStatus.TODO
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()
        subject = mock_notification_service.send_email.call_args[0][1]
        assert subject == "New Task Created"

    def test_create_task_with_duplicate_title_fails(self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = Task("Existing Task")

        with pytest.raises(ValueError, match="already exists"):
            task_service.create_task("Existing Task")

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_create_task_with_invalid_title_never_touches_collaborators(
        self, task_service, mock_repository, mock_notification_service
    ):
        with pytest.raises(ValueError, match="at least 3 characters"):
            task_service.create_task("ab")

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_create_task_with_past_due_date_fails(self, task_service, mock_repository, past):
        with pytest.raises(ValueError, match="must be in the future"):
            task_service.create_task("Late task", due_date=past)

        mock_repository.save.assert_not_called()

    def test_create_task_uses_real_clock_when_none_is_injected(self, mock_repository, mock_notification_service):
        from datetime import datetime

        mock_repository.find_by_title.return_value = None
        service = TaskService(mock_repository, mock_notification_service)

        task = service.create_task("Real clock", due_date=datetime.now() + timedelta(days=1))

        assert task.due_date is not None

    def test_urgent_task_also_sends_sms(self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None

        task_service.create_task_with_sms("Server down", priority=TaskPriority.URGENT)

        mock_notification_service.send_email.assert_called_once()
        mock_notification_service.send_sms.assert_called_once()

    def test_non_urgent_task_does_not_send_sms(self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None

        task_service.create_task_with_sms("Water plants", priority=TaskPriority.LOW)

        mock_notification_service.send_email.assert_called_once()
        mock_notification_service.send_sms.assert_not_called()


class TestStatusWorkflow:
    def test_update_task_status_triggers_notification(self, task_service, mock_repository, mock_notification_service):
        task = Task("Test Task")
        mock_repository.find_by_id.return_value = task

        updated = task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        assert updated.status == TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once_with(task)
        recipient, subject, body = mock_notification_service.send_email.call_args[0]
        assert recipient == "user@example.com"
        assert subject == "Task Status Updated"
        assert "TODO" in body and "IN_PROGRESS" in body

    def test_complete_workflow_todo_to_done(self, task_service, mock_repository, mock_notification_service):
        task = Task("Complete workflow task")
        mock_repository.find_by_id.return_value = task

        task_service.update_task_status(1, TaskStatus.IN_PROGRESS)
        task_service.update_task_status(1, TaskStatus.DONE)

        assert task.status == TaskStatus.DONE
        assert mock_repository.save.call_count == 2
        assert mock_notification_service.send_email.call_count == 2

    def test_update_task_with_invalid_transition_fails(self, task_service, mock_repository, mock_notification_service):
        task = Task("Test Task")
        task.status = TaskStatus.DONE
        mock_repository.find_by_id.return_value = task

        with pytest.raises(ValueError, match="Invalid transition"):
            task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        assert task.status == TaskStatus.DONE
        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_update_status_of_missing_task_fails(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            task_service.update_task_status(99, TaskStatus.IN_PROGRESS)

        mock_repository.save.assert_not_called()

    def test_update_status_rejects_non_status_values(self, task_service, mock_repository):
        with pytest.raises(ValueError, match="Invalid status"):
            task_service.update_task_status(1, "DONE")

        mock_repository.find_by_id.assert_not_called()


class TestArchiveAndDelete:
    def test_delete_task_marks_as_archived(self, fake_service):
        service, repository, notifier = fake_service
        task = service.create_task("Disposable task")
        notifier.reset_mock()

        archived = service.delete_task(task.id)

        assert archived.status == TaskStatus.ARCHIVED
        assert repository.find_by_id(task.id).status == TaskStatus.ARCHIVED
        notifier.send_email.assert_called_once()

    def test_archive_task_prevents_further_updates(self, fake_service):
        service, _, _ = fake_service
        task = service.create_task("Archive me")
        service.delete_task(task.id)

        with pytest.raises(ValueError, match="Archived tasks cannot be modified"):
            service.update_task(task.id, description="too late")
        with pytest.raises(ValueError, match="Invalid transition"):
            service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

    def test_archived_task_cannot_be_archived_twice(self, fake_service):
        service, _, _ = fake_service
        task = service.create_task("Archive once")
        service.delete_task(task.id)

        with pytest.raises(ValueError, match="Invalid transition"):
            service.delete_task(task.id)

    def test_purge_removes_only_archived_tasks(self, fake_service):
        service, repository, _ = fake_service
        task = service.create_task("Purge me")
        service.delete_task(task.id)

        assert service.purge_task(task.id) is True
        assert repository.find_by_id(task.id) is None

    def test_purge_refuses_tasks_that_are_not_archived(self, fake_service):
        service, repository, _ = fake_service
        task = service.create_task("Keep me")

        with pytest.raises(ValueError, match="Only archived tasks"):
            service.purge_task(task.id)

        assert repository.find_by_id(task.id) is task

    def test_purge_of_missing_task_fails(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            task_service.purge_task(5)

        mock_repository.delete.assert_not_called()


class TestUpdateTask:
    def test_update_task_changes_every_editable_field(self, fake_service, now):
        service, _, _ = fake_service
        task = service.create_task("Original title")
        new_due = now + timedelta(days=30)

        updated = service.update_task(
            task.id,
            title="Renamed task",
            description="New description",
            priority=TaskPriority.URGENT,
            due_date=new_due,
        )

        assert updated.title == "Renamed task"
        assert updated.description == "New description"
        assert updated.priority == TaskPriority.URGENT
        assert updated.due_date == new_due
        assert updated.updated_at == now

    def test_update_task_keeps_fields_that_are_not_supplied(self, fake_service):
        service, _, _ = fake_service
        task = service.create_task("Stable title", "Stable text", TaskPriority.HIGH)

        updated = service.update_task(task.id, priority=TaskPriority.LOW)

        assert updated.title == "Stable title"
        assert updated.description == "Stable text"
        assert updated.priority == TaskPriority.LOW

    def test_update_task_may_keep_its_own_title(self, fake_service):
        service, _, _ = fake_service
        task = service.create_task("Same title")

        assert service.update_task(task.id, title="Same title").title == "Same title"

    def test_update_task_rejects_title_used_by_another_task(self, fake_service):
        service, _, _ = fake_service
        service.create_task("Taken title")
        other = service.create_task("Other title")

        with pytest.raises(ValueError, match="already exists"):
            service.update_task(other.id, title="Taken title")

        assert other.title == "Other title"

    def test_failed_update_changes_nothing(self, fake_service, past):
        service, _, _ = fake_service
        task = service.create_task("Atomic update", priority=TaskPriority.LOW)

        with pytest.raises(ValueError, match="must be in the future"):
            service.update_task(task.id, priority=TaskPriority.URGENT, due_date=past)

        assert task.priority == TaskPriority.LOW

    def test_update_task_rejects_invalid_priority(self, fake_service):
        service, _, _ = fake_service
        task = service.create_task("Priority check")

        with pytest.raises(ValueError, match="TaskPriority"):
            service.update_task(task.id, priority="HIGH")

    def test_update_of_missing_task_fails(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            task_service.update_task(7, title="Does not matter")

    def test_get_task_returns_stored_task(self, fake_service):
        service, _, _ = fake_service
        task = service.create_task("Fetch me")

        assert service.get_task(task.id) is task

    def test_get_task_raises_for_unknown_id(self, fake_service):
        service, _, _ = fake_service

        with pytest.raises(ValueError, match="not found"):
            service.get_task(404)


class TestOverdueDetection:
    def test_overdue_task_detection_triggers_notification(
        self, task_service, mock_repository, mock_notification_service, now
    ):
        overdue = Task("Overdue task", now=now)
        overdue.due_date = now - timedelta(days=1)
        upcoming = Task("Future task", now=now)
        upcoming.due_date = now + timedelta(days=1)
        mock_repository.find_all.return_value = [overdue, upcoming]

        result = task_service.check_overdue_tasks()

        assert result == [overdue]
        mock_notification_service.send_email.assert_called_once()
        assert "overdue" in mock_notification_service.send_email.call_args[0][2].lower()

    def test_completed_and_archived_tasks_are_never_reported_overdue(
        self, task_service, mock_repository, mock_notification_service, now
    ):
        done = Task("Finished task", now=now)
        done.due_date = now - timedelta(days=3)
        done.status = TaskStatus.DONE
        archived = Task("Archived task", now=now)
        archived.due_date = now - timedelta(days=3)
        archived.status = TaskStatus.ARCHIVED
        mock_repository.find_all.return_value = [done, archived]

        assert task_service.check_overdue_tasks() == []
        mock_notification_service.send_email.assert_not_called()

    def test_each_overdue_task_gets_its_own_notification(
        self, task_service, mock_repository, mock_notification_service, now
    ):
        tasks = []
        for name in ("First late", "Second late", "Third late"):
            task = Task(name, now=now)
            task.due_date = now - timedelta(hours=1)
            tasks.append(task)
        mock_repository.find_all.return_value = tasks

        task_service.check_overdue_tasks()

        assert mock_notification_service.send_email.call_count == 3


class TestSearchAndFilter:
    @pytest.fixture
    def populated(self, fake_service, now):
        service, _, _ = fake_service
        service.create_task("Write report", priority=TaskPriority.HIGH, due_date=now + timedelta(days=2))
        service.create_task("Write tests", priority=TaskPriority.URGENT, due_date=now + timedelta(days=10))
        service.create_task("Buy milk", priority=TaskPriority.LOW)
        started = service.create_task("Read book", priority=TaskPriority.HIGH)
        service.update_task_status(started.id, TaskStatus.IN_PROGRESS)
        return service

    def test_search_tasks_by_status(self, populated):
        titles = [t.title for t in populated.search_tasks(status=TaskStatus.IN_PROGRESS)]
        assert titles == ["Read book"]

    def test_filter_tasks_by_priority(self, populated):
        titles = {t.title for t in populated.search_tasks(priority=TaskPriority.HIGH)}
        assert titles == {"Write report", "Read book"}

    def test_search_by_partial_title_is_case_insensitive(self, populated):
        titles = {t.title for t in populated.search_tasks(title_contains="WRITE")}
        assert titles == {"Write report", "Write tests"}

    def test_filter_by_due_date_range(self, populated, now):
        titles = [
            t.title for t in populated.search_tasks(due_from=now + timedelta(days=1), due_to=now + timedelta(days=5))
        ]
        assert titles == ["Write report"]

    def test_combined_filters_must_all_match(self, populated):
        results = populated.search_tasks(title_contains="write", priority=TaskPriority.URGENT, status=TaskStatus.TODO)
        assert [t.title for t in results] == ["Write tests"]

    def test_results_are_ordered_by_priority(self, populated):
        priorities = [t.priority for t in populated.search_tasks()]
        assert priorities == sorted(priorities, key=lambda p: p.value, reverse=True)

    def test_search_without_matches_returns_empty_list(self, populated):
        assert populated.search_tasks(title_contains="nothing like this") == []
