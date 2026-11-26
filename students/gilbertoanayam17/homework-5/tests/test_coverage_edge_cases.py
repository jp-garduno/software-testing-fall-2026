"""Edge cases written from the coverage report: each test targets a branch or boundary still uncovered."""

import pytest

from notification_service import NotificationError, NotificationService
from task import Task, TaskPriority, TaskStateError
from task_repository import TaskFilter
from task_service import TaskService


class TestTaskFilterBranches:
    def test_filter_without_criteria_matches_any_task(self):
        assert TaskFilter().matches(Task("No due date")) is True

    def test_filter_rejects_inverted_date_range(self, clock):
        with pytest.raises(ValueError, match="due_from must not be later than due_to"):
            TaskFilter(due_from=clock.in_days(5), due_to=clock.in_days(1))

    def test_filter_accepts_single_day_range(self, clock):
        day = clock.in_days(2)
        assert TaskFilter(due_from=day, due_to=day).matches(Task("Exactly that day", due_date=day)) is True

    def test_filter_excludes_task_due_before_range(self, clock):
        task = Task("Too early", due_date=clock.in_days(1))
        assert TaskFilter(due_from=clock.in_days(2)).matches(task) is False

    def test_filter_excludes_task_due_after_range(self, clock):
        task = Task("Too late", due_date=clock.in_days(9))
        assert TaskFilter(due_to=clock.in_days(5)).matches(task) is False

    def test_filter_with_only_start_date_has_no_upper_bound(self, clock):
        task = Task("Far future", due_date=clock.in_days(400))
        assert TaskFilter(due_from=clock.in_days(1)).matches(task) is True

    def test_filter_excludes_task_without_due_date_when_range_given(self, clock):
        assert TaskFilter(due_to=clock.in_days(5)).matches(Task("Someday")) is False

    def test_filter_excludes_on_priority_mismatch(self):
        task = Task("Low priority", priority=TaskPriority.LOW)
        assert TaskFilter(priority=TaskPriority.HIGH).matches(task) is False


class TestRepositoryBranches:
    def test_save_existing_task_updates_instead_of_inserting(self, fake_repository):
        task = fake_repository.save(Task("Saved once"))
        task.description = "edited"

        fake_repository.save(task)

        assert len(fake_repository.find_all()) == 1
        assert fake_repository.find_by_id(task.id).description == "edited"

    def test_find_by_title_ignores_case_and_surrounding_spaces(self, fake_repository):
        task = fake_repository.save(Task("Weekly Report"))
        assert fake_repository.find_by_title("  weekly report ") is task

    def test_find_by_title_returns_none_for_partial_match(self, fake_repository):
        fake_repository.save(Task("Weekly Report"))
        assert fake_repository.find_by_title("Weekly") is None

    def test_delete_reports_whether_something_was_removed(self, fake_repository):
        task = fake_repository.save(Task("Delete me"))
        assert fake_repository.delete(task.id) is True
        assert fake_repository.delete(task.id) is False


class TestServiceBranches:
    def test_purge_of_active_task_is_rejected(self, service, mock_repository):
        mock_repository.find_by_id.return_value = Task("Still active")

        with pytest.raises(TaskStateError, match="Only archived tasks"):
            service.purge_task(1)

        mock_repository.delete.assert_not_called()

    def test_deleting_an_archived_task_again_fails(self, fake_service):
        task = fake_service.create_task("Archive twice")
        fake_service.delete_task(task.id)

        with pytest.raises(TaskStateError, match="from ARCHIVED to ARCHIVED"):
            fake_service.delete_task(task.id)

    def test_update_may_keep_the_task_own_title(self, fake_service):
        task = fake_service.create_task("Keep my title")

        fake_service.update_task(task.id, title="KEEP MY TITLE")

        assert fake_service.get_task(task.id).title == "KEEP MY TITLE"

    def test_update_without_new_title_skips_uniqueness_check(self, service, mock_repository):
        mock_repository.find_by_id.return_value = Task("Untouched title")

        service.update_task(1, priority=TaskPriority.HIGH)

        mock_repository.find_by_title.assert_not_called()

    def test_urgent_task_without_phone_sends_email_only(self, mock_repository, mock_notifier):
        service = TaskService(mock_repository, mock_notifier)

        service.create_task("Urgent but no phone", priority=TaskPriority.URGENT)

        mock_notifier.send_email.assert_called_once()
        mock_notifier.send_sms.assert_not_called()


class TestBoundaryValues:
    def test_title_is_measured_after_stripping_spaces(self):
        assert Task("  abc  ").title == "abc"

    def test_update_rejects_past_due_date(self, clock):
        task = Task("Reschedule me", due_date=clock.in_days(3))
        with pytest.raises(ValueError, match="must be in the future"):
            task.update(due_date=clock.in_days(-1))
        assert task.due_date == clock.in_days(3)

    def test_transition_to_unknown_status_value_is_rejected(self):
        with pytest.raises(TaskStateError, match="from TODO to DONE"):
            Task("Raw string status").transition_to("DONE")

    def test_sms_of_exactly_160_characters_is_not_truncated(self, notifier, http_client):
        notifier.send_sms("+523312345678", "y" * 160)

        assert http_client.post.call_args.kwargs["json"]["message"] == "y" * 160

    def test_http_400_is_the_first_status_treated_as_failure(self, notifier, http_client):
        """Added after a mutant (>= 400 changed to > 400) survived despite 100% branch coverage."""
        http_client.post.return_value.status_code = 400

        with pytest.raises(NotificationError, match="HTTP 400"):
            notifier.send_email("ana@example.com", "Hello", "Body")

    def test_gateway_url_trailing_slash_is_normalized(self, http_client):
        NotificationService(http_client, base_url="https://gateway.test/").send_email("a@b.co", "S", "B")

        assert http_client.post.call_args.args[0] == "https://gateway.test/email"
