"""Part 4: Tests demonstrating mocking, test isolation, stubs, fakes, and error scenarios."""

import time
from unittest.mock import ANY, Mock, call
import pytest
from notification_service import NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import TaskRepository
from task_service import TaskService


class TestMockInteractionsAndVerifications:
    """Tests demonstrating mock behavior verification, call arguments, and ordering."""

    def test_verify_mock_call_count(self, task_service, mock_repository, mock_notification_service):
        """Verify exact call count on mocked repository and notification service."""
        mock_repository.find_by_title.return_value = None

        task_service.create_task("Verify Count Task")

        assert mock_repository.save.call_count == 1
        assert mock_notification_service.send_email.call_count == 1
        assert mock_notification_service.send_sms.call_count == 0

    def test_verify_mock_call_arguments(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Verify mock called with exact arguments and ANY matcher."""
        mock_repository.find_by_title.return_value = None

        created = task_service.create_task("Argument Check Task", recipient_email="boss@example.com")

        mock_repository.save.assert_called_with(created)
        mock_notification_service.send_email.assert_called_with(
            "boss@example.com",
            "New Task Created",
            ANY,
        )

    def test_verify_call_ordering_save_before_notification(
        self, mock_repository, mock_notification_service
    ):
        """Verify that task persistence strictly occurs before notification dispatch."""
        parent_mock = Mock()
        parent_mock.attach_mock(mock_repository.save, "repo_save")
        parent_mock.attach_mock(mock_notification_service.send_email, "notify_email")

        mock_repository.find_by_title.return_value = None
        service = TaskService(mock_repository, mock_notification_service)

        service.create_task("Order Verification Task")

        # Confirm call sequence
        expected_calls = [
            call.repo_save(ANY),
            call.notify_email(ANY, ANY, ANY),
        ]
        parent_mock.assert_has_calls(expected_calls, any_order=False)


class TestTestDoubleTypes:
    """Demonstrate differences between Mocks, Stubs, and Fakes."""

    def test_stub_returns_predefined_responses(self, mock_repository):
        """Stub returns deterministic canned responses without external database."""
        stubbed_task = Task("Stubbed Task", task_id=77)
        mock_repository.find_by_id.return_value = stubbed_task
        mock_repository.find_by_title.return_value = None

        assert mock_repository.find_by_id(77) == stubbed_task
        assert mock_repository.find_by_title("Unknown") is None

    def test_fake_in_memory_repository(self, fake_repository, mock_notification_service):
        """Fake test double provides working in-memory persistence without a real database."""
        service = TaskService(fake_repository, mock_notification_service)

        task1 = service.create_task("Fake Task 1", priority=TaskPriority.HIGH)
        task2 = service.create_task("Fake Task 2", priority=TaskPriority.LOW)

        assert task1.id is not None
        assert task2.id is not None
        assert fake_repository.find_by_id(task1.id) == task1
        assert len(fake_repository.find_all()) == 2

        # Demonstrate deletion using fake
        fake_repository.delete(task1.id)
        assert fake_repository.find_by_id(task1.id) is None
        assert len(fake_repository.find_all()) == 1


class TestErrorScenariosWithMocks:
    """Test error handling and failure resilience using mocked side effects."""

    def test_repository_failure_handled_gracefully(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Handle repository failure gracefully: raise error and abort notification."""
        mock_repository.find_by_title.return_value = None
        mock_repository.save.side_effect = Exception("Database connection failed")

        with pytest.raises(Exception, match="Database connection failed"):
            task_service.create_task("Test Task")

        mock_notification_service.send_email.assert_not_called()

    def test_notification_failure_does_not_break_workflow(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Notification failure should not prevent task creation."""
        mock_repository.find_by_title.return_value = None
        mock_notification_service.send_email.side_effect = Exception("SMTP server unavailable")

        task = task_service.create_task("Test Task")

        assert task.title == "Test Task"
        mock_repository.save.assert_called_once()
        mock_notification_service.send_email.assert_called_once()

    def test_notification_failure_on_status_update_does_not_break_update(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Notification failure during status change does not revert status change."""
        task = Task("Status Task")
        mock_repository.find_by_id.return_value = task
        mock_notification_service.send_email.side_effect = Exception("SMS/Email network timeout")

        updated = task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        assert updated.status == TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once()
        mock_notification_service.send_email.assert_called_once()

    def test_multiple_notification_channels_urgent_task(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Urgent task creation triggers both email and SMS notifications."""
        mock_repository.find_by_title.return_value = None

        task = task_service.create_task_with_sms(
            "Urgent Task",
            priority=TaskPriority.URGENT,
            phone_number="+15551234567",
        )

        assert task.title == "Urgent Task"
        assert mock_notification_service.send_email.called
        assert mock_notification_service.send_sms.called
        mock_notification_service.send_sms.assert_called_with(
            "+15551234567",
            "Urgent task created: Urgent Task",
        )


class TestTestIsolationAndPerformance:
    """Verify isolation and execution speed (< 1 second requirement)."""

    def test_execution_speed_benchmark(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Ensure full execution cycle runs in less than 50 milliseconds."""
        mock_repository.find_by_title.return_value = None
        start = time.perf_counter()

        for i in range(20):
            mock_repository.find_by_title.return_value = None
            task_service.create_task(f"Speed Task {i}")

        elapsed = time.perf_counter() - start
        assert elapsed < 0.5  # Fast execution well below 1 second threshold
