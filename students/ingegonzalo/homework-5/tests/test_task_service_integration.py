from datetime import datetime, timedelta

import pytest

from task import TaskPriority, TaskStatus


class TestCreateTask:
    def test_create_task_success_with_notification(
            self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None

        task = task_service.create_task("Write tests", "Unit tests", TaskPriority.HIGH)

        assert task.title == "Write tests"
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()
        assert "New Task Created" in mock_notification_service.send_email.call_args[0][1]

    def test_create_task_with_duplicate_title_fails(
            self, task_service, mock_repository, mock_notification_service, make_task):
        mock_repository.find_by_title.return_value = make_task("Existing Task")

        with pytest.raises(ValueError, match="already exists"):
            task_service.create_task("Existing Task")

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_create_task_with_past_due_date_fails(
            self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None

        with pytest.raises(ValueError, match="in the future"):
            task_service.create_task("Past task", due_date=datetime.now() - timedelta(days=1))

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_create_urgent_task_sends_sms(
            self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None

        task_service.create_task_with_sms("Urgent Task", priority=TaskPriority.URGENT)

        mock_notification_service.send_email.assert_called_once()
        mock_notification_service.send_sms.assert_called_once()

    def test_create_non_urgent_task_does_not_send_sms(
            self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None

        task_service.create_task_with_sms("Normal Task", priority=TaskPriority.LOW)

        mock_notification_service.send_sms.assert_not_called()


class TestStatusUpdates:
    def test_update_task_status_triggers_notification(
            self, task_service, mock_repository, mock_notification_service, make_task):
        mock_repository.find_by_id.return_value = make_task("Test Task")

        updated = task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        assert updated.status == TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once()
        args = mock_notification_service.send_email.call_args[0]
        assert "Status Updated" in args[1]
        assert "TODO" in args[2] and "IN_PROGRESS" in args[2]

    def test_complete_workflow_todo_to_done(
            self, task_service, mock_repository, mock_notification_service, make_task):
        mock_repository.find_by_id.return_value = make_task("Workflow task")

        task = task_service.update_task_status(1, TaskStatus.IN_PROGRESS)
        assert task.status == TaskStatus.IN_PROGRESS
        task = task_service.update_task_status(1, TaskStatus.DONE)
        assert task.status == TaskStatus.DONE

        assert mock_repository.save.call_count == 2
        assert mock_notification_service.send_email.call_count == 2

    def test_update_task_with_invalid_transition_fails(
            self, task_service, mock_repository, mock_notification_service, make_task):
        mock_repository.find_by_id.return_value = make_task("Done Task", status=TaskStatus.DONE)

        with pytest.raises(ValueError, match="Invalid transition"):
            task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_update_status_of_missing_task_fails(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            task_service.update_task_status(99, TaskStatus.DONE)

    def test_archive_task_prevents_further_updates(
            self, task_service, mock_repository, make_task):
        mock_repository.find_by_id.return_value = make_task("Old", status=TaskStatus.ARCHIVED)

        with pytest.raises(ValueError, match="Invalid transition"):
            task_service.update_task_status(1, TaskStatus.IN_PROGRESS)
        with pytest.raises(ValueError, match="archived"):
            task_service.update_task(1, description="new text")

        mock_repository.save.assert_not_called()


class TestUpdateFields:
    def test_update_all_fields(self, task_service, mock_repository, make_task):
        task = make_task("Old title")
        mock_repository.find_by_id.return_value = task
        mock_repository.find_by_title.return_value = None
        due = datetime.now() + timedelta(days=3)

        updated = task_service.update_task(
            1, title="New title", description="desc",
            priority=TaskPriority.URGENT, due_date=due)

        assert (updated.title, updated.description) == ("New title", "desc")
        assert updated.priority == TaskPriority.URGENT
        assert updated.due_date == due
        mock_repository.save.assert_called_once_with(task)

    def test_update_title_to_duplicate_fails(self, task_service, mock_repository, make_task):
        mock_repository.find_by_id.return_value = make_task("Mine")
        mock_repository.find_by_title.return_value = make_task("Taken")

        with pytest.raises(ValueError, match="already exists"):
            task_service.update_task(1, title="Taken")
        mock_repository.save.assert_not_called()

    def test_update_title_to_same_title_is_allowed(self, task_service, mock_repository, make_task):
        task = make_task("Same title")
        mock_repository.find_by_id.return_value = task
        mock_repository.find_by_title.return_value = task

        assert task_service.update_task(1, title="Same title").title == "Same title"

    def test_update_with_invalid_due_date_changes_nothing(
            self, task_service, mock_repository, make_task):
        task = make_task("Keep me")
        mock_repository.find_by_id.return_value = task
        mock_repository.find_by_title.return_value = None

        with pytest.raises(ValueError, match="in the future"):
            task_service.update_task(1, title="Changed",
                                     due_date=datetime.now() - timedelta(days=1))

        assert task.title == "Keep me"
        mock_repository.save.assert_not_called()


class TestDelete:
    def test_delete_task_marks_as_archived(
            self, task_service, mock_repository, mock_notification_service, make_task):
        mock_repository.find_by_id.return_value = make_task("To delete")

        task = task_service.delete_task(1)

        assert task.status == TaskStatus.ARCHIVED
        mock_repository.save.assert_called_once_with(task)
        mock_repository.delete.assert_not_called()  # soft delete
        mock_notification_service.send_email.assert_called_once()

    def test_delete_already_archived_fails(self, task_service, mock_repository, make_task):
        mock_repository.find_by_id.return_value = make_task("Gone", status=TaskStatus.ARCHIVED)
        with pytest.raises(ValueError, match="already archived"):
            task_service.delete_task(1)

    def test_delete_missing_task_fails(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = None
        with pytest.raises(ValueError, match="not found"):
            task_service.delete_task(42)


class TestSearchAndFilter:
    @pytest.fixture
    def populated(self, mock_repository, make_task):
        now = datetime.now()
        tasks = [
            make_task("Write report", TaskStatus.TODO, TaskPriority.HIGH, now + timedelta(days=2)),
            make_task("Review code", TaskStatus.IN_PROGRESS, TaskPriority.LOW, now + timedelta(days=10)),
            make_task("Deploy app", TaskStatus.DONE, TaskPriority.HIGH, None),
        ]
        mock_repository.find_all.return_value = tasks
        return tasks

    def test_search_tasks_by_status(self, task_service, populated):
        assert task_service.search_tasks(status=TaskStatus.DONE) == [populated[2]]

    def test_filter_tasks_by_priority(self, task_service, populated):
        assert task_service.search_tasks(priority=TaskPriority.HIGH) == [populated[0], populated[2]]

    def test_filter_by_date_range(self, task_service, populated):
        now = datetime.now()
        result = task_service.search_tasks(due_from=now, due_to=now + timedelta(days=5))
        assert result == [populated[0]]

    def test_filter_due_to_excludes_later_tasks(self, task_service, populated):
        result = task_service.search_tasks(due_to=datetime.now() + timedelta(days=1))
        assert result == []

    def test_search_by_partial_title_case_insensitive(self, task_service, populated):
        assert task_service.search_tasks(title_contains="REVIEW") == [populated[1]]

    def test_combined_filters(self, task_service, populated):
        result = task_service.search_tasks(
            status=TaskStatus.TODO, priority=TaskPriority.HIGH, title_contains="report")
        assert result == [populated[0]]

    def test_no_filters_returns_everything(self, task_service, populated):
        assert len(task_service.search_tasks()) == 3


class TestOverdue:
    def test_overdue_task_detection_triggers_notification(
            self, task_service, mock_repository, mock_notification_service, make_task):
        late = make_task("Late", due_date=datetime.now() - timedelta(days=1))
        ok = make_task("Fine", due_date=datetime.now() + timedelta(days=1))
        mock_repository.find_all.return_value = [late, ok]

        result = task_service.check_overdue_tasks()

        assert result == [late]
        mock_notification_service.send_email.assert_called_once()
        assert "overdue" in mock_notification_service.send_email.call_args[0][2].lower()

    def test_no_overdue_tasks_sends_nothing(
            self, task_service, mock_repository, mock_notification_service, make_task):
        mock_repository.find_all.return_value = [make_task("Fine")]
        assert task_service.check_overdue_tasks() == []
        mock_notification_service.send_email.assert_not_called()