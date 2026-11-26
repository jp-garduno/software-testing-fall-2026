"""Part 4: test doubles (mock / stub / fake), error scenarios and isolation."""

import time
from unittest.mock import ANY, Mock

import pytest

from notification_service import NotificationError, NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import RepositoryError, TaskRepository
from task_service import TaskService


class FakeTaskRepository:
    """Fake: a small but working in-memory repository."""

    def __init__(self):
        self.tasks = {}
        self._next_id = 1

    def save(self, task):
        if task.id is None:
            task.id = self._next_id
            self._next_id += 1
        self.tasks[task.id] = task
        return task

    def find_by_id(self, task_id):
        return self.tasks.get(task_id)

    def find_by_title(self, title):
        return next((t for t in self.tasks.values() if t.title == title), None)

    def find_all(self):
        return list(self.tasks.values())

    def search(self, **filters):
        return [t for t in self.tasks.values() if filters.get("status") in (None, t.status)]


# ---------------------------------------------------------------- stubs
class TestStubs:
    """Stubs only provide canned answers; we assert on the result."""

    def test_stub_not_found_allows_creation(self, task_service, mock_repository):
        mock_repository.find_by_title.return_value = None
        assert task_service.create_task("Brand new").title == "Brand new"

    def test_stub_found_blocks_creation(self, task_service, mock_repository):
        mock_repository.find_by_title.return_value = Task("Brand new")
        with pytest.raises(ValueError):
            task_service.create_task("Brand new")

    def test_stub_with_side_effect_sequence(self, task_service, mock_repository):
        mock_repository.find_by_title.side_effect = [None, Task("Twice")]
        task_service.create_task("Twice")
        with pytest.raises(ValueError, match="already exists"):
            task_service.create_task("Twice")


# ---------------------------------------------------------------- mocks
class TestMockVerification:
    """Mocks verify behaviour: calls, arguments, counts and ordering."""

    def test_call_arguments_are_verified(self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None

        task_service.create_task("Verify args")

        mock_repository.find_by_title.assert_called_once_with("Verify args")
        mock_notification_service.send_email.assert_called_once_with(
            "user@example.com", "New Task Created", ANY
        )

    def test_call_count_matches_number_of_operations(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None
        for name in ("Task one", "Task two", "Task three"):
            task_service.create_task(name)

        assert mock_repository.save.call_count == 3
        assert mock_notification_service.send_email.call_count == 3

    def test_save_happens_before_notification(self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None
        order = []
        mock_repository.save.side_effect = lambda task: order.append("save")
        mock_notification_service.send_email.side_effect = lambda *a: order.append("email")

        task_service.create_task("Ordered")

        assert order == ["save", "email"]

    def test_mock_spec_rejects_unknown_methods(self, mock_repository):
        with pytest.raises(AttributeError):
            mock_repository.does_not_exist()


# ---------------------------------------------------------------- errors
class TestErrorScenarios:
    def test_repository_failure_handled_gracefully(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None
        mock_repository.save.side_effect = RepositoryError("Database connection failed")

        with pytest.raises(RepositoryError, match="Database connection failed"):
            task_service.create_task("Test Task")

        mock_notification_service.send_email.assert_not_called()

    def test_repository_lookup_failure_propagates(self, task_service, mock_repository):
        mock_repository.find_by_id.side_effect = RepositoryError("read failed")

        with pytest.raises(RepositoryError):
            task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

    def test_notification_failure_does_not_break_workflow(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None
        mock_notification_service.send_email.side_effect = Exception("SMTP server unavailable")

        task = task_service.create_task("Test Task")

        assert task.title == "Test Task"
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()

    def test_notification_failure_during_status_update_keeps_change(
        self, task_service, mock_repository, mock_notification_service
    ):
        task = Task("Keep change")
        mock_repository.find_by_id.return_value = task
        mock_notification_service.send_email.side_effect = NotificationError("down")

        assert task_service.update_task_status(1, TaskStatus.IN_PROGRESS).status == TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once_with(task)

    def test_notification_failure_during_overdue_check_still_returns_tasks(
        self, task_service, mock_repository, mock_notification_service
    ):
        from datetime import datetime, timedelta

        late = Task("Late")
        late.due_date = datetime.now() - timedelta(hours=1)
        mock_repository.find_all.return_value = [late]
        mock_notification_service.send_email.side_effect = Exception("boom")

        assert task_service.check_overdue_tasks() == [late]


# ---------------------------------------------------------------- multiple channels
class TestMultipleChannels:
    def test_multiple_notification_channels_for_urgent_task(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None

        task_service.create_task_with_sms("Urgent Task", priority=TaskPriority.URGENT)

        mock_notification_service.send_email.assert_called_once()
        mock_notification_service.send_sms.assert_called_once_with("+521234567890", ANY)

    def test_non_urgent_task_does_not_send_sms(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None

        task_service.create_task_with_sms("Calm task", priority=TaskPriority.MEDIUM)

        mock_notification_service.send_email.assert_called_once()
        mock_notification_service.send_sms.assert_not_called()

    def test_sms_failure_does_not_break_urgent_creation(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None
        mock_notification_service.send_sms.side_effect = NotificationError("no signal")

        task = task_service.create_task_with_sms("Urgent Task", priority=TaskPriority.URGENT)

        assert task.priority == TaskPriority.URGENT


# ---------------------------------------------------------------- fakes
class TestFakeRepository:
    """With a fake we can run a whole workflow and assert on the final state."""

    @pytest.fixture
    def service(self, mock_notification_service):
        return TaskService(FakeTaskRepository(), mock_notification_service)

    def test_full_lifecycle_with_fake_repository(self, service, mock_notification_service):
        task = service.create_task("Lifecycle", priority=TaskPriority.HIGH)
        assert task.id == 1

        service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        service.update_task_status(task.id, TaskStatus.DONE)
        service.delete_task(task.id)

        assert service.get_task(task.id).status == TaskStatus.ARCHIVED
        assert mock_notification_service.send_email.call_count == 4

    def test_duplicate_detection_with_fake_repository(self, service):
        service.create_task("Unique")
        with pytest.raises(ValueError, match="already exists"):
            service.create_task("Unique")

    def test_search_with_fake_repository(self, service):
        first = service.create_task("First one")
        service.create_task("Second one")
        service.update_task_status(first.id, TaskStatus.IN_PROGRESS)

        found = service.search_tasks(status=TaskStatus.IN_PROGRESS)

        assert [t.title for t in found] == ["First one"]


# ---------------------------------------------------------------- isolation
class TestIsolationAndSpeed:
    def test_tests_do_not_share_state_first(self, mock_repository):
        mock_repository.save(Task("Shared?"))
        assert mock_repository.save.call_count == 1

    def test_tests_do_not_share_state_second(self, mock_repository):
        # A fresh mock per test: the call from the previous test is not visible.
        assert mock_repository.save.call_count == 0

    def test_service_never_touches_real_providers(self, mock_repository):
        """A real NotificationService without transport would raise: it must be mocked."""
        mock_repository.find_by_title.return_value = None
        real = NotificationService()  # no transport configured
        service = TaskService(mock_repository, real)

        # The failure is swallowed by the service, proving the workflow survives it.
        assert service.create_task("Isolated").title == "Isolated"

    def test_service_operations_run_fast(self, task_service, mock_repository):
        mock_repository.find_by_title.return_value = None
        start = time.perf_counter()
        for i in range(200):
            task_service.create_task(f"Speed task {i}")
        assert time.perf_counter() - start < 1.0

    def test_repository_wraps_database_errors(self):
        broken = Mock()
        broken.get.side_effect = OSError("disk gone")
        with pytest.raises(RepositoryError):
            TaskRepository(broken).find_by_id(1)
