from datetime import datetime, timedelta

import pytest
from task import Task, TaskPriority, TaskStatus


# ---------------- Creación ----------------
class TestCreateTask:
    def test_create_task_success_with_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None

        task = task_service.create_task(
            "Write tests", "Unit and integration", TaskPriority.HIGH
        )

        assert task.title == "Write tests"
        assert task.status == TaskStatus.TODO
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()
        assert (
            "New Task Created" in mock_notification_service.send_email.call_args[0][1]
        )

    def test_create_task_with_duplicate_title_fails(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = Task("Existing Task")

        with pytest.raises(ValueError, match="already exists"):
            task_service.create_task("Existing Task")

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_create_task_with_invalid_title_does_not_save(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None

        with pytest.raises(ValueError, match="at least 3 characters"):
            task_service.create_task("ab")

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_create_task_with_past_due_date_fails(self, task_service, mock_repository):
        mock_repository.find_by_title.return_value = None

        with pytest.raises(ValueError, match="must be in the future"):
            task_service.create_task(
                "Valid title", due_date=datetime.now() - timedelta(days=1)
            )

        mock_repository.save.assert_not_called()


# ---------------- Estados ----------------
class TestUpdateStatus:
    def test_update_task_status_triggers_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        task = Task("Test Task")
        mock_repository.find_by_id.return_value = task

        updated = task_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        assert updated.status == TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()
        args = mock_notification_service.send_email.call_args[0]
        assert "Status Updated" in args[1]
        assert "TODO" in args[2]
        assert "IN_PROGRESS" in args[2]

    def test_complete_workflow_todo_to_done(
        self, task_service, mock_repository, mock_notification_service
    ):
        task = Task("Complete workflow task")
        mock_repository.find_by_id.return_value = task

        task_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        task_service.update_task_status(task.id, TaskStatus.DONE)

        assert task.status == TaskStatus.DONE
        assert mock_repository.save.call_count == 2
        assert mock_notification_service.send_email.call_count == 2

    def test_update_task_with_invalid_transition_fails(
        self, task_service, mock_repository, mock_notification_service
    ):
        task = Task("Test Task")
        task.status = TaskStatus.DONE
        mock_repository.find_by_id.return_value = task

        with pytest.raises(ValueError, match="Invalid transition"):
            task_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_update_status_of_missing_task_fails(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            task_service.update_task_status("missing-id", TaskStatus.DONE)

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()


# ---------------- Actualización de campos ----------------
class TestUpdateTask:
    def test_update_task_fields_saves_task(self, task_service, mock_repository, future):
        task = Task("Old title")
        mock_repository.find_by_id.return_value = task
        mock_repository.find_by_title.return_value = None

        updated = task_service.update_task(
            task.id,
            title="New title",
            description="Desc",
            priority=TaskPriority.URGENT,
            due_date=future,
        )

        assert updated.title == "New title"
        assert updated.priority == TaskPriority.URGENT
        assert updated.due_date == future
        mock_repository.save.assert_called_once_with(task)

    def test_update_task_with_duplicate_title_fails(
        self, task_service, mock_repository
    ):
        task = Task("Task one")
        other = Task("Task two")
        mock_repository.find_by_id.return_value = task
        mock_repository.find_by_title.return_value = other

        with pytest.raises(ValueError, match="already exists"):
            task_service.update_task(task.id, title="Task two")

        mock_repository.save.assert_not_called()

    def test_update_task_with_same_title_is_allowed(
        self, task_service, mock_repository
    ):
        task = Task("Same title")
        mock_repository.find_by_id.return_value = task

        task_service.update_task(task.id, title="Same title", description="Changed")

        mock_repository.find_by_title.assert_not_called()
        mock_repository.save.assert_called_once_with(task)

    def test_update_task_keeping_own_title_found_is_allowed(
        self, task_service, mock_repository
    ):
        task = Task("Original")
        mock_repository.find_by_id.return_value = task
        mock_repository.find_by_title.return_value = task  # mismo id

        task_service.update_task(task.id, title="Renamed")

        mock_repository.save.assert_called_once_with(task)

    def test_archive_task_prevents_further_updates(self, task_service, mock_repository):
        task = Task("Archived task")
        task.archive()
        mock_repository.find_by_id.return_value = task

        with pytest.raises(ValueError, match="archived"):
            task_service.update_task(task.id, description="Nope")

        mock_repository.save.assert_not_called()

    def test_update_missing_task_fails(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            task_service.update_task("missing-id", description="x")


# ---------------- Eliminación ----------------
class TestDeleteTask:
    def test_delete_task_marks_as_archived(self, task_service, mock_repository):
        task = Task("Delete me")
        mock_repository.find_by_id.return_value = task

        result = task_service.delete_task(task.id)

        assert result.status == TaskStatus.ARCHIVED
        mock_repository.save.assert_called_once_with(task)
        mock_repository.delete.assert_not_called()  # soft delete, no borrado físico

    def test_delete_already_archived_task_fails(self, task_service, mock_repository):
        task = Task("Already archived")
        task.archive()
        mock_repository.find_by_id.return_value = task

        with pytest.raises(ValueError, match="Invalid transition"):
            task_service.delete_task(task.id)

        mock_repository.save.assert_not_called()


# ---------------- Vencimiento ----------------
class TestOverdue:
    def test_overdue_task_detection_triggers_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        overdue = Task("Overdue task")
        overdue.due_date = datetime.now() - timedelta(days=1)
        fine = Task("Future task")
        fine.due_date = datetime.now() + timedelta(days=1)
        mock_repository.find_all.return_value = [overdue, fine]

        result = task_service.check_overdue_tasks()

        assert result == [overdue]
        mock_notification_service.send_email.assert_called_once()
        assert "overdue" in mock_notification_service.send_email.call_args[0][2].lower()

    def test_check_overdue_with_no_overdue_tasks_sends_nothing(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_all.return_value = [Task("Fine task")]

        assert task_service.check_overdue_tasks() == []
        mock_notification_service.send_email.assert_not_called()


# ---------------- Búsqueda y filtros ----------------
@pytest.fixture
def sample_tasks():
    now = datetime.now()
    a = Task("Buy milk", priority=TaskPriority.LOW, due_date=now + timedelta(days=1))
    b = Task(
        "Write report", priority=TaskPriority.HIGH, due_date=now + timedelta(days=5)
    )
    c = Task("Buy gifts", priority=TaskPriority.HIGH)  # sin fecha
    b.status = TaskStatus.IN_PROGRESS
    return a, b, c


class TestSearchAndFilter:
    def test_search_tasks_by_status(self, task_service, mock_repository, sample_tasks):
        a, b, c = sample_tasks
        mock_repository.find_all.return_value = [a, b, c]

        assert task_service.search_tasks(status=TaskStatus.IN_PROGRESS) == [b]

    def test_filter_tasks_by_priority(
        self, task_service, mock_repository, sample_tasks
    ):
        a, b, c = sample_tasks
        mock_repository.find_all.return_value = [a, b, c]

        assert task_service.search_tasks(priority=TaskPriority.HIGH) == [b, c]

    def test_filter_tasks_by_date_range(
        self, task_service, mock_repository, sample_tasks
    ):
        a, b, c = sample_tasks
        mock_repository.find_all.return_value = [a, b, c]
        now = datetime.now()

        assert task_service.search_tasks(due_from=now + timedelta(days=3)) == [b]
        assert task_service.search_tasks(due_to=now + timedelta(days=3)) == [a]
        assert task_service.search_tasks(
            due_from=now, due_to=now + timedelta(days=10)
        ) == [a, b]

    def test_search_tasks_by_partial_title_case_insensitive(
        self, task_service, mock_repository, sample_tasks
    ):
        a, b, c = sample_tasks
        mock_repository.find_all.return_value = [a, b, c]

        assert task_service.search_tasks(title="BUY") == [a, c]

    def test_search_tasks_with_combined_filters(
        self, task_service, mock_repository, sample_tasks
    ):
        a, b, c = sample_tasks
        mock_repository.find_all.return_value = [a, b, c]

        result = task_service.search_tasks(priority=TaskPriority.HIGH, title="buy")

        assert result == [c]

    def test_search_tasks_without_filters_returns_all(
        self, task_service, mock_repository, sample_tasks
    ):
        mock_repository.find_all.return_value = list(sample_tasks)

        assert task_service.search_tasks() == list(sample_tasks)
