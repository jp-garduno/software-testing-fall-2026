import logging
from unittest.mock import ANY

import pytest
from notification_service import NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import TaskRepository
from task_service import DEFAULT_EMAIL, DEFAULT_PHONE, TaskService


# ======================================================================
# FAKE: implementación simplificada que sí funciona (en memoria)
# ======================================================================
class FakeTaskRepository:
    def __init__(self):
        self.tasks = {}

    def save(self, task):
        self.tasks[task.id] = task

    def find_by_id(self, task_id):
        return self.tasks.get(task_id)

    def find_by_title(self, title):
        return next((t for t in self.tasks.values() if t.title == title), None)

    def find_all(self):
        return list(self.tasks.values())

    def delete(self, task_id):
        self.tasks.pop(task_id, None)


# ======================================================================
# MOCKS: verificación de interacciones
# ======================================================================
class TestMockVerification:
    def test_email_called_with_exact_arguments(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None

        task_service.create_task("Exact args")

        mock_notification_service.send_email.assert_called_once_with(
            DEFAULT_EMAIL, "New Task Created", "Task 'Exact args' has been created"
        )

    def test_email_called_with_any_body(
        self, task_service, mock_repository, mock_notification_service
    ):
        task = Task("Any body")
        mock_repository.find_by_id.return_value = task

        task_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        mock_notification_service.send_email.assert_called_with(
            DEFAULT_EMAIL, "Task Status Updated", ANY
        )

    def test_repository_is_queried_by_title_before_saving(
        self, task_service, mock_repository
    ):
        mock_repository.find_by_title.return_value = None

        task_service.create_task("Query first")

        mock_repository.find_by_title.assert_called_once_with("Query first")

    def test_save_happens_before_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        order = []
        mock_repository.find_by_title.return_value = None
        mock_repository.save.side_effect = lambda t: order.append("save")
        mock_notification_service.send_email.side_effect = lambda *a: order.append(
            "email"
        )

        task_service.create_task("Ordered task")

        assert order == ["save", "email"]

    def test_notification_not_sent_when_nothing_overdue(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_all.return_value = []

        task_service.check_overdue_tasks()

        mock_notification_service.send_email.assert_not_called()
        mock_notification_service.send_sms.assert_not_called()


# ======================================================================
# STUBS: respuestas predefinidas
# ======================================================================
class TestStubs:
    def test_get_task_returns_stubbed_task(self, task_service, mock_repository):
        task = Task("Stubbed task")
        mock_repository.find_by_id.return_value = task

        assert task_service.get_task(task.id) is task
        mock_repository.find_by_id.assert_called_once_with(task.id)

    def test_get_task_not_found_raises(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            task_service.get_task("nope")


# ======================================================================
# ERRORES: fallos de repositorio
# ======================================================================
class TestRepositoryFailures:
    def test_repository_failure_handled_gracefully(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None
        mock_repository.save.side_effect = Exception("Database connection failed")

        with pytest.raises(Exception, match="Database connection failed"):
            task_service.create_task("Test Task")

        mock_notification_service.send_email.assert_not_called()

    def test_lookup_failure_prevents_save_and_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.side_effect = Exception("DB timeout")

        with pytest.raises(Exception, match="DB timeout"):
            task_service.create_task("Test Task")

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_save_failure_on_status_update_sends_no_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        task = Task("Status fail")
        mock_repository.find_by_id.return_value = task
        mock_repository.save.side_effect = Exception("Disk full")

        with pytest.raises(Exception, match="Disk full"):
            task_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        mock_notification_service.send_email.assert_not_called()

    def test_find_all_failure_propagates_in_overdue_check(
        self, task_service, mock_repository
    ):
        mock_repository.find_all.side_effect = Exception("DB down")

        with pytest.raises(Exception, match="DB down"):
            task_service.check_overdue_tasks()


# ======================================================================
# ERRORES: fallos de notificación (no deben romper el flujo)
# ======================================================================
class TestNotificationFailures:
    def test_notification_failure_does_not_break_workflow(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None
        mock_notification_service.send_email.side_effect = Exception(
            "SMTP server unavailable"
        )

        task = task_service.create_task("Test Task")

        assert task.title == "Test Task"
        mock_repository.save.assert_called_once()
        mock_notification_service.send_email.assert_called_once()

    def test_notification_failure_on_status_update_still_saves(
        self, task_service, mock_repository, mock_notification_service
    ):
        task = Task("Notify fail")
        mock_repository.find_by_id.return_value = task
        mock_notification_service.send_email.side_effect = Exception("SMTP down")

        updated = task_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        assert updated.status == TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once_with(task)

    def test_notification_failure_is_logged(
        self, task_service, mock_repository, mock_notification_service, caplog
    ):
        mock_repository.find_by_title.return_value = None
        mock_notification_service.send_email.side_effect = Exception("SMTP down")

        with caplog.at_level(logging.WARNING):
            task_service.create_task("Logged failure")

        assert "Email notification failed" in caplog.text

    def test_overdue_check_continues_when_notification_fails(
        self, task_service, mock_repository, mock_notification_service
    ):
        from datetime import datetime, timedelta

        t1, t2 = Task("Overdue one"), Task("Overdue two")
        t1.due_date = t2.due_date = datetime.now() - timedelta(days=1)
        mock_repository.find_all.return_value = [t1, t2]
        mock_notification_service.send_email.side_effect = Exception("SMTP down")

        result = task_service.check_overdue_tasks()

        assert result == [t1, t2]
        assert mock_notification_service.send_email.call_count == 2


# ======================================================================
# MÚLTIPLES CANALES (email + SMS)
# ======================================================================
class TestMultipleChannels:
    def test_urgent_task_sends_email_and_sms(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None

        task = task_service.create_task_with_sms(
            "Urgent Task", priority=TaskPriority.URGENT
        )

        assert task.priority == TaskPriority.URGENT
        mock_notification_service.send_email.assert_called_once()
        mock_notification_service.send_sms.assert_called_once_with(
            DEFAULT_PHONE, "URGENT task created: 'Urgent Task'"
        )

    @pytest.mark.parametrize(
        "priority", [TaskPriority.LOW, TaskPriority.MEDIUM, TaskPriority.HIGH]
    )
    def test_non_urgent_task_sends_only_email(
        self, task_service, mock_repository, mock_notification_service, priority
    ):
        mock_repository.find_by_title.return_value = None

        task_service.create_task_with_sms("Normal Task", priority=priority)

        mock_notification_service.send_email.assert_called_once()
        mock_notification_service.send_sms.assert_not_called()

    def test_sms_failure_does_not_break_urgent_creation(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None
        mock_notification_service.send_sms.side_effect = Exception("SMS gateway down")

        task = task_service.create_task_with_sms(
            "Urgent Task", priority=TaskPriority.URGENT
        )

        assert task.title == "Urgent Task"
        mock_repository.save.assert_called_once()
        mock_notification_service.send_sms.assert_called_once()

    def test_duplicate_urgent_task_sends_no_sms(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = Task("Urgent Task")

        with pytest.raises(ValueError, match="already exists"):
            task_service.create_task_with_sms(
                "Urgent Task", priority=TaskPriority.URGENT
            )

        mock_notification_service.send_sms.assert_not_called()


# ======================================================================
# FAKE en acción: flujo completo sin mocks de repositorio
# ======================================================================
class TestFakeRepositoryWorkflow:
    @pytest.fixture
    def fake_service(self, mock_notification_service):
        return TaskService(FakeTaskRepository(), mock_notification_service)

    def test_full_lifecycle_with_fake_repository(self, fake_service):
        task = fake_service.create_task("Lifecycle", priority=TaskPriority.HIGH)

        fake_service.update_task(task.id, description="Updated")
        fake_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        fake_service.update_task_status(task.id, TaskStatus.DONE)
        fake_service.delete_task(task.id)

        stored = fake_service.get_task(task.id)
        assert stored.description == "Updated"
        assert stored.status == TaskStatus.ARCHIVED

    def test_fake_repository_rejects_duplicate_titles(self, fake_service):
        fake_service.create_task("Unique title")

        with pytest.raises(ValueError, match="already exists"):
            fake_service.create_task("Unique title")

    def test_fake_repository_search_by_status(self, fake_service):
        a = fake_service.create_task("Task alpha")
        fake_service.create_task("Task beta")
        fake_service.update_task_status(a.id, TaskStatus.IN_PROGRESS)

        result = fake_service.search_tasks(status=TaskStatus.IN_PROGRESS)

        assert [t.title for t in result] == ["Task alpha"]

    def test_fake_repository_delete_removes_task(self):
        repo = FakeTaskRepository()
        task = Task("Remove me")
        repo.save(task)

        repo.delete(task.id)

        assert repo.find_by_id(task.id) is None


# ======================================================================
# INTERFACES: deben ser implementadas o mockeadas
# ======================================================================
class TestInterfacesMustBeImplemented:
    @pytest.mark.parametrize(
        "call",
        [
            lambda r: r.save(Task("Some task")),
            lambda r: r.find_by_id("1"),
            lambda r: r.find_by_title("x"),
            lambda r: r.find_all(),
            lambda r: r.delete("1"),
        ],
    )
    def test_repository_methods_raise_not_implemented(self, call):
        with pytest.raises(NotImplementedError):
            call(TaskRepository())

    def test_repository_keeps_database_reference(self):
        db = object()
        assert TaskRepository(db).database is db

    def test_notification_send_email_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            NotificationService().send_email("a@b.com", "s", "b")

    def test_notification_send_sms_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            NotificationService().send_sms("+52123", "msg")
