from datetime import datetime, timedelta

import pytest
from task import Task, TaskPriority, TaskStatus


# ---------------- Task: casos borde ----------------
class TestTaskEdgeCases:
    def test_description_none_becomes_empty_string(self):
        assert Task("Some task", description=None).description == ""

    def test_description_exactly_500_chars_is_kept(self):
        assert len(Task("Some task", "z" * 500).description) == 500

    def test_update_only_priority(self):
        t = Task("Some task", description="keep")
        t.update(priority=TaskPriority.MEDIUM)
        assert t.priority == TaskPriority.MEDIUM
        assert t.description == "keep"
        assert t.title == "Some task"

    def test_update_description_to_empty_string(self):
        t = Task("Some task", description="old")
        t.update(description="")
        assert t.description == ""

    def test_update_changes_updated_at(self):
        t = Task("Some task")
        before = t.updated_at
        t.update(description="new")
        assert t.updated_at >= before

    def test_archived_update_checked_before_validation(self):
        t = Task("Some task")
        t.archive()
        with pytest.raises(ValueError, match="archived"):
            t.update(title="ab")  # título inválido, pero gana el error de archivado

    def test_in_progress_task_past_due_is_overdue(self):
        t = Task("Some task")
        t.status = TaskStatus.IN_PROGRESS
        t.due_date = datetime.now() - timedelta(seconds=1)
        assert t.is_overdue() is True

    def test_invalid_title_does_not_leave_partial_update(self):
        t = Task("Original")
        with pytest.raises(ValueError):
            t.update(title="x", description="should not apply")
        assert t.description == ""

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (TaskPriority.URGENT, TaskPriority.LOW, 1),
            (TaskPriority.LOW, TaskPriority.URGENT, -1),
            (TaskPriority.MEDIUM, TaskPriority.MEDIUM, 0),
            (TaskPriority.HIGH, TaskPriority.MEDIUM, 1),
        ],
    )
    def test_compare_priority_matrix(self, a, b, expected):
        assert (
            Task("Task A", priority=a).compare_priority(Task("Task B", priority=b))
            == expected
        )

    def test_priority_sorting_order(self):
        tasks = [
            Task("Low", priority=TaskPriority.LOW),
            Task("Urgent", priority=TaskPriority.URGENT),
            Task("Medium", priority=TaskPriority.MEDIUM),
            Task("High", priority=TaskPriority.HIGH),
        ]
        ordered = sorted(tasks, key=lambda t: t.priority.value, reverse=True)
        assert [t.title for t in ordered] == ["Urgent", "High", "Medium", "Low"]


# ---------------- TaskService: ramas restantes ----------------
class TestServiceEdgeCases:
    def test_update_task_without_title_skips_duplicate_check(
        self, task_service, mock_repository
    ):
        task = Task("Some task")
        mock_repository.find_by_id.return_value = task

        task_service.update_task(task.id, priority=TaskPriority.HIGH)

        mock_repository.find_by_title.assert_not_called()
        assert task.priority == TaskPriority.HIGH

    def test_update_task_does_not_send_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        task = Task("Some task")
        mock_repository.find_by_id.return_value = task

        task_service.update_task(task.id, description="quiet")

        mock_notification_service.send_email.assert_not_called()

    def test_delete_done_task_archives_it(self, task_service, mock_repository):
        task = Task("Done task")
        task.status = TaskStatus.DONE
        mock_repository.find_by_id.return_value = task

        assert task_service.delete_task(task.id).status == TaskStatus.ARCHIVED

    def test_delete_missing_task_fails(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            task_service.delete_task("missing")

    @pytest.mark.parametrize(
        "status", [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]
    )
    def test_status_update_to_archived_from_any_state_notifies(
        self, task_service, mock_repository, mock_notification_service, status
    ):
        task = Task("Some task")
        task.status = status
        mock_repository.find_by_id.return_value = task

        task_service.update_task_status(task.id, TaskStatus.ARCHIVED)

        assert task.status == TaskStatus.ARCHIVED
        mock_notification_service.send_email.assert_called_once()

    def test_overdue_check_ignores_done_and_archived(
        self, task_service, mock_repository, mock_notification_service
    ):
        past = datetime.now() - timedelta(days=2)
        done, archived = Task("Done task"), Task("Archived task")
        done.due_date = archived.due_date = past
        done.status = TaskStatus.DONE
        archived.status = TaskStatus.ARCHIVED
        mock_repository.find_all.return_value = [done, archived]

        assert task_service.check_overdue_tasks() == []
        mock_notification_service.send_email.assert_not_called()

    def test_overdue_check_sends_one_email_per_overdue_task(
        self, task_service, mock_repository, mock_notification_service
    ):
        past = datetime.now() - timedelta(days=1)
        tasks = [Task(f"Late task {i}") for i in range(3)]
        for t in tasks:
            t.due_date = past
        mock_repository.find_all.return_value = tasks

        assert len(task_service.check_overdue_tasks()) == 3
        assert mock_notification_service.send_email.call_count == 3

    def test_search_with_empty_title_returns_all(self, task_service, mock_repository):
        tasks = [Task("Task one"), Task("Task two")]
        mock_repository.find_all.return_value = tasks

        assert task_service.search_tasks(title="") == tasks

    def test_search_date_filters_exclude_tasks_without_due_date(
        self, task_service, mock_repository
    ):
        no_date = Task("No date")
        mock_repository.find_all.return_value = [no_date]

        assert task_service.search_tasks(due_from=datetime.now()) == []
        assert task_service.search_tasks(due_to=datetime.now()) == []

    def test_search_with_no_matches_returns_empty_list(
        self, task_service, mock_repository
    ):
        mock_repository.find_all.return_value = [Task("Buy milk")]

        assert task_service.search_tasks(title="zzz") == []

    def test_search_on_empty_repository(self, task_service, mock_repository):
        mock_repository.find_all.return_value = []

        assert task_service.search_tasks(status=TaskStatus.DONE) == []
