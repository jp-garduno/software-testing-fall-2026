from datetime import timedelta

import pytest
from doubles import OWNER_EMAIL, OWNER_PHONE, START

from notification_service import GatewayError, NotificationError, NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import TaskFilter
from task_service import DuplicateTitleError, TaskService

ONE_MICROSECOND = timedelta(microseconds=1)


class TestTitleAndDescriptionBoundaries:
    @pytest.mark.parametrize("length", [3, 100])
    def test_title_at_length_limit_is_accepted(self, length):
        assert len(Task("t" * length).title) == length

    def test_title_padding_does_not_count_towards_minimum(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("  ab  ")

    def test_title_padding_does_not_count_towards_maximum(self):
        assert len(Task("  " + "t" * 100 + "  ").title) == 100

    def test_description_of_exactly_500_characters_is_accepted(self):
        assert len(Task("Write tests", "d" * 500).description) == 500


class TestTimeBoundaries:
    def test_due_date_equal_to_now_is_rejected(self, clock):
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Write tests", due_date=clock.now)

    def test_due_date_one_microsecond_after_now_is_accepted(self, clock):
        task = Task("Write tests", due_date=clock.now + ONE_MICROSECOND)

        assert task.due_date == clock.now + ONE_MICROSECOND

    def test_task_is_not_overdue_at_the_exact_due_instant(self, clock, make_task):
        task = make_task(due_date=clock.now + timedelta(days=1))
        clock.advance(days=1)

        assert task.is_overdue() is False

    def test_task_is_overdue_one_microsecond_after_the_due_instant(self, clock, make_task):
        task = make_task(due_date=clock.now + timedelta(days=1))
        clock.advance(days=1, microseconds=1)

        assert task.is_overdue() is True


class TestUpdateDetailsBranches:
    @pytest.mark.parametrize(
        "field, value",
        [
            ("title", "Renamed task"),
            ("description", "A new description"),
            ("priority", TaskPriority.URGENT),
            ("due_date", START + timedelta(days=3)),
        ],
    )
    def test_update_details_with_a_single_field_changes_only_that_field(self, clock, make_task, field, value):
        task = make_task(description="Original", due_date=clock.now + timedelta(days=1))
        before = vars(task).copy()

        task.update_details(**{field: value})

        changed = {name for name in vars(task) if vars(task)[name] != before[name]}
        assert changed == {field}

    def test_update_details_with_empty_description_clears_it(self, make_task):
        task = make_task(description="Something to remove")

        task.update_details(description="")

        assert task.description == ""

    @pytest.mark.parametrize("status", [TaskStatus.IN_PROGRESS, TaskStatus.DONE])
    def test_update_details_is_allowed_before_archiving(self, make_task, status):
        task = make_task(status)

        task.update_details(priority=TaskPriority.HIGH)

        assert task.priority == TaskPriority.HIGH


class TestTaskFilterBranches:
    def test_filter_rejects_due_from_later_than_due_to(self):
        with pytest.raises(ValueError, match="due_from must not be later than due_to"):
            TaskFilter(due_from=START + timedelta(days=2), due_to=START + timedelta(days=1))

    def test_filter_with_equal_due_from_and_due_to_matches_that_instant(self, clock, make_task):
        due = clock.now + timedelta(days=1)
        task = make_task(due_date=due)

        assert TaskFilter(due_from=due, due_to=due).matches(task) is True

    @pytest.mark.parametrize("offset_days, expected", [(1, False), (2, True), (3, True)])
    def test_filter_with_only_due_from_is_inclusive(self, clock, make_task, offset_days, expected):
        task = make_task(due_date=clock.now + timedelta(days=offset_days))

        assert TaskFilter(due_from=clock.now + timedelta(days=2)).matches(task) is expected

    @pytest.mark.parametrize("offset_days, expected", [(1, True), (2, True), (3, False)])
    def test_filter_with_only_due_to_is_inclusive(self, clock, make_task, offset_days, expected):
        task = make_task(due_date=clock.now + timedelta(days=offset_days))

        assert TaskFilter(due_to=clock.now + timedelta(days=2)).matches(task) is expected

    def test_date_range_excludes_tasks_without_due_date(self, make_task):
        assert TaskFilter(due_to=START + timedelta(days=30)).matches(make_task()) is False

    def test_filter_without_date_range_keeps_tasks_without_due_date(self, make_task):
        assert TaskFilter(status=TaskStatus.TODO).matches(make_task()) is True

    @pytest.mark.parametrize("title_contains", ["", "   "])
    def test_blank_title_search_matches_every_task(self, make_task, title_contains):
        assert TaskFilter(title_contains=title_contains).matches(make_task()) is True

    def test_title_search_ignores_case_and_surrounding_spaces(self, make_task):
        task = make_task(title="Write Unit Tests")

        assert TaskFilter(title_contains="  unit TESTS ").matches(task) is True

    def test_status_filter_rejects_other_statuses_even_when_other_criteria_match(self, make_task):
        task = make_task(TaskStatus.DONE, priority=TaskPriority.HIGH)

        assert TaskFilter(status=TaskStatus.TODO, priority=TaskPriority.HIGH).matches(task) is False


class TestRepositoryLookupBranches:
    def test_find_by_title_without_match_returns_none(self, repository):
        repository.save(Task("Write tests"))

        assert repository.find_by_title("Write test") is None

    def test_search_keeps_insertion_order_between_equal_priorities(self, repository):
        first = repository.save(Task("First medium", priority=TaskPriority.MEDIUM))
        urgent = repository.save(Task("Only urgent", priority=TaskPriority.URGENT))
        second = repository.save(Task("Second medium", priority=TaskPriority.MEDIUM))

        assert repository.search(TaskFilter()) == [urgent, first, second]


class TestNotificationBoundaries:
    def test_sms_of_exactly_160_characters_is_sent_unchanged(self, notification_service, sms_gateway):
        message = "m" * 160

        notification_service.send_sms(OWNER_PHONE, message)

        sms_gateway.send.assert_called_once_with(OWNER_PHONE, message)

    def test_sms_of_161_characters_is_cut_to_160_with_ellipsis(self, notification_service, sms_gateway):
        notification_service.send_sms(OWNER_PHONE, "m" * 161)

        sms_gateway.send.assert_called_once_with(OWNER_PHONE, "m" * 157 + "...")

    @pytest.mark.parametrize(
        "address",
        ["", None, "owner", "owner@", "@taskflow.test", "owner@taskflow", "own er@taskflow.test", "a@b@taskflow.test"],
    )
    def test_malformed_email_address_is_rejected(self, notification_service, email_gateway, address):
        with pytest.raises(ValueError, match="Invalid email address"):
            notification_service.send_email(address, "Subject", "Body")
        email_gateway.send.assert_not_called()

    @pytest.mark.parametrize(
        "phone_number",
        ["", None, "3312345678", "+0331234567", "+52 33 1234 5678", "+1234567", "+1234567890123456"],
    )
    def test_malformed_phone_number_is_rejected(self, notification_service, sms_gateway, phone_number):
        with pytest.raises(ValueError, match="Invalid phone number"):
            notification_service.send_sms(phone_number, "Message")
        sms_gateway.send.assert_not_called()

    @pytest.mark.parametrize("phone_number", ["+12345678", "+123456789012345"])
    def test_phone_number_at_e164_length_limit_is_accepted(self, notification_service, sms_gateway, phone_number):
        notification_service.send_sms(phone_number, "Message")

        sms_gateway.send.assert_called_once_with(phone_number, "Message")

    @pytest.mark.parametrize("max_attempts", [0, -1])
    def test_max_attempts_below_one_is_rejected(self, email_gateway, sms_gateway, max_attempts):
        with pytest.raises(ValueError, match="max_attempts must be at least 1"):
            NotificationService(email_gateway, sms_gateway, max_attempts=max_attempts)

    def test_single_attempt_service_does_not_retry(self, email_gateway, sms_gateway):
        email_gateway.send.side_effect = GatewayError("timeout")
        notification_service = NotificationService(email_gateway, sms_gateway, max_attempts=1)

        with pytest.raises(NotificationError, match="after 1 attempts"):
            notification_service.send_email(OWNER_EMAIL, "Subject", "Body")
        email_gateway.send.assert_called_once()


class TestServiceConfigurationBranches:
    def test_service_rejects_malformed_owner_email(self, mock_repository, notifier):
        with pytest.raises(ValueError, match="Invalid email address"):
            TaskService(mock_repository, notifier, "owner-at-taskflow")

    def test_service_rejects_malformed_owner_phone(self, mock_repository, notifier):
        with pytest.raises(ValueError, match="Invalid phone number"):
            TaskService(mock_repository, notifier, OWNER_EMAIL, "33 1234 5678")

    def test_urgent_task_without_owner_phone_is_notified_by_email_only(self, mock_repository, notifier):
        mock_repository.find_by_title.return_value = None
        service = TaskService(mock_repository, notifier, OWNER_EMAIL)

        service.create_task("Fix production bug", priority=TaskPriority.URGENT)

        notifier.send_email.assert_called_once()
        notifier.send_sms.assert_not_called()

    @pytest.mark.parametrize("priority", [TaskPriority.LOW, TaskPriority.MEDIUM, TaskPriority.HIGH])
    def test_non_urgent_task_is_never_sent_by_sms(self, mocked_service, mock_repository, notifier, priority):
        mock_repository.find_by_title.return_value = None

        mocked_service.create_task("Plan sprint", priority=priority)

        notifier.send_sms.assert_not_called()


class TestRenameBranches:
    @pytest.fixture(name="stored_task")
    def fixture_stored_task(self, mock_repository):
        task = Task("Write tests")
        task.task_id = 7
        mock_repository.find_by_id.return_value = task
        return task

    def test_rename_to_a_free_title_is_saved(self, mocked_service, mock_repository, stored_task):
        mock_repository.find_by_title.return_value = None

        mocked_service.update_task(7, title="Write more tests")

        mock_repository.save.assert_called_once_with(stored_task)

    def test_rename_to_own_title_with_different_case_is_allowed(self, mocked_service, mock_repository, stored_task):
        mock_repository.find_by_title.return_value = stored_task

        mocked_service.update_task(7, title="WRITE TESTS")

        assert stored_task.title == "WRITE TESTS"

    def test_rename_to_title_of_another_task_is_rejected(self, mocked_service, mock_repository, stored_task):
        other = Task("Run tests")
        other.task_id = 8
        mock_repository.find_by_title.return_value = other

        with pytest.raises(DuplicateTitleError):
            mocked_service.update_task(7, title="Run tests")
        assert stored_task.title == "Write tests"

    def test_update_without_title_skips_the_uniqueness_check(self, mocked_service, mock_repository, stored_task):
        mocked_service.update_task(7, priority=TaskPriority.HIGH)

        mock_repository.find_by_title.assert_not_called()
        assert stored_task.priority == TaskPriority.HIGH
