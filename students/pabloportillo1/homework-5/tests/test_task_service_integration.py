from datetime import timedelta

import pytest
from doubles import OWNER_EMAIL, OWNER_PHONE

from task import ArchivedTaskError, InvalidTransitionError, TaskPriority, TaskStatus
from task_repository import TaskFilter
from task_service import DuplicateTitleError, TaskNotFoundError


def email_subjects(notifier):
    return [sent.args[1] for sent in notifier.send_email.call_args_list]


class TestTaskCreation:
    def test_create_task_success_with_notification(self, service, repository, notifier):
        task = service.create_task("Write tests", "Unit and integration tests", TaskPriority.HIGH)

        assert repository.find_by_id(task.task_id) is task
        notifier.send_email.assert_called_once_with(
            OWNER_EMAIL, "New Task Created", "Task 'Write tests' has been created"
        )

    def test_create_task_assigns_a_new_id_to_each_task(self, service):
        first = service.create_task("Write tests")
        second = service.create_task("Run tests")

        assert (first.task_id, second.task_id) == (1, 2)

    def test_create_task_with_duplicate_title_fails(self, service, repository, notifier):
        service.create_task("Write tests")
        notifier.reset_mock()

        with pytest.raises(DuplicateTitleError, match="already exists"):
            service.create_task("  WRITE TESTS ")
        assert len(repository.find_all()) == 1
        notifier.send_email.assert_not_called()

    def test_create_task_with_invalid_data_stores_and_sends_nothing(self, service, repository, notifier):
        with pytest.raises(ValueError, match="at least 3 characters"):
            service.create_task("ab")
        assert repository.find_all() == []
        notifier.send_email.assert_not_called()

    def test_create_urgent_task_notifies_by_email_and_sms(self, service, notifier):
        service.create_task("Fix production bug", priority=TaskPriority.URGENT)

        notifier.send_email.assert_called_once()
        notifier.send_sms.assert_called_once_with(
            OWNER_PHONE, "New Task Created: Task 'Fix production bug' has been created"
        )


class TestStatusWorkflow:
    def test_update_task_status_triggers_notification(self, service, notifier):
        task = service.create_task("Write tests")
        notifier.reset_mock()

        service.update_task_status(task.task_id, TaskStatus.IN_PROGRESS)

        notifier.send_email.assert_called_once_with(
            OWNER_EMAIL, "Task Status Updated", "Task 'Write tests' changed from TODO to IN_PROGRESS"
        )

    def test_complete_workflow_todo_to_done(self, service, repository, notifier):
        task = service.create_task("Write tests")

        service.update_task_status(task.task_id, TaskStatus.IN_PROGRESS)
        service.update_task_status(task.task_id, TaskStatus.DONE)

        assert repository.find_by_id(task.task_id).status == TaskStatus.DONE
        assert email_subjects(notifier) == ["New Task Created", "Task Status Updated", "Task Status Updated"]

    def test_update_task_with_invalid_transition_fails(self, service, repository, notifier):
        task = service.create_task("Write tests")
        service.update_task_status(task.task_id, TaskStatus.IN_PROGRESS)
        service.update_task_status(task.task_id, TaskStatus.DONE)
        notifier.reset_mock()

        with pytest.raises(InvalidTransitionError, match="from DONE to IN_PROGRESS"):
            service.update_task_status(task.task_id, TaskStatus.IN_PROGRESS)
        assert repository.find_by_id(task.task_id).status == TaskStatus.DONE
        notifier.send_email.assert_not_called()

    def test_update_status_of_unknown_task_raises_not_found(self, service):
        with pytest.raises(TaskNotFoundError, match="Task 99 not found"):
            service.update_task_status(99, TaskStatus.IN_PROGRESS)


class TestEditingWorkflow:
    def test_update_task_changes_fields_and_persists(self, clock, service, repository):
        task = service.create_task("Write tests")
        clock.advance(hours=1)

        service.update_task(task.task_id, title="Write more tests", priority=TaskPriority.HIGH)

        stored = repository.find_by_id(task.task_id)
        assert (stored.title, stored.priority, stored.updated_at) == ("Write more tests", TaskPriority.HIGH, clock.now)

    def test_update_task_to_title_of_another_task_fails(self, service, repository):
        service.create_task("Write tests")
        task = service.create_task("Run tests")

        with pytest.raises(DuplicateTitleError, match="already exists"):
            service.update_task(task.task_id, title="write tests")
        assert repository.find_by_id(task.task_id).title == "Run tests"

    def test_archive_task_prevents_further_updates(self, service):
        task = service.create_task("Write tests")
        service.delete_task(task.task_id)

        with pytest.raises(ArchivedTaskError, match="cannot be modified"):
            service.update_task(task.task_id, description="Too late")

    def test_archived_task_cannot_be_restored(self, service):
        task = service.create_task("Write tests")
        service.delete_task(task.task_id)

        with pytest.raises(InvalidTransitionError, match="from ARCHIVED to TODO"):
            service.update_task_status(task.task_id, TaskStatus.TODO)


class TestDeletion:
    def test_delete_task_marks_as_archived(self, service, repository, notifier):
        task = service.create_task("Write tests")

        service.delete_task(task.task_id)

        assert repository.find_by_id(task.task_id).status == TaskStatus.ARCHIVED
        notifier.send_email.assert_called_with(
            OWNER_EMAIL, "Task Status Updated", "Task 'Write tests' changed from TODO to ARCHIVED"
        )

    def test_purged_task_cannot_be_recovered(self, service):
        task = service.create_task("Write tests")
        service.delete_task(task.task_id)

        service.purge_task(task.task_id)

        with pytest.raises(TaskNotFoundError):
            service.get_task(task.task_id)

    def test_purge_frees_the_title_for_a_new_task(self, service):
        task = service.create_task("Write tests")
        service.purge_task(task.task_id)

        recreated = service.create_task("Write tests")

        assert recreated.task_id != task.task_id


class TestOverdueDetection:
    def test_overdue_task_detection_triggers_notification(self, clock, service, notifier):
        late = service.create_task("Submit homework", due_date=clock.now + timedelta(days=1))
        service.create_task("Prepare exam", due_date=clock.now + timedelta(days=10))
        finished = service.create_task("Read chapter", due_date=clock.now + timedelta(days=1))
        service.update_task_status(finished.task_id, TaskStatus.IN_PROGRESS)
        service.update_task_status(finished.task_id, TaskStatus.DONE)
        notifier.reset_mock()
        clock.advance(days=2)

        overdue = service.check_overdue_tasks()

        assert overdue == [late]
        notifier.send_email.assert_called_once_with(
            OWNER_EMAIL, "Task Overdue", "Task 'Submit homework' is overdue (due 2026-10-20 09:00)"
        )

    def test_urgent_overdue_task_is_also_sent_by_sms(self, clock, service, notifier):
        service.create_task("Renew passport", priority=TaskPriority.URGENT, due_date=clock.now + timedelta(hours=1))
        notifier.reset_mock()
        clock.advance(hours=2)

        service.check_overdue_tasks()

        notifier.send_sms.assert_called_once_with(
            OWNER_PHONE, "Task Overdue: Task 'Renew passport' is overdue (due 2026-10-19 10:00)"
        )


class TestSearchAndFilter:
    @pytest.fixture
    def board(self, clock, service):
        """Five tasks in TODO, IN_PROGRESS and DONE, covering every priority, due 1-10 days out or never."""
        tasks = {
            "unit": service.create_task(
                "Write unit tests", priority=TaskPriority.HIGH, due_date=clock.now + timedelta(days=3)
            ),
            "integration": service.create_task(
                "Write integration tests", priority=TaskPriority.URGENT, due_date=clock.now + timedelta(days=5)
            ),
            "flaky": service.create_task(
                "Fix flaky test", priority=TaskPriority.MEDIUM, due_date=clock.now + timedelta(days=1)
            ),
            "sprint": service.create_task("Plan sprint"),
            "readme": service.create_task(
                "Update README", priority=TaskPriority.MEDIUM, due_date=clock.now + timedelta(days=10)
            ),
        }
        service.update_task_status(tasks["integration"].task_id, TaskStatus.IN_PROGRESS)
        service.update_task_status(tasks["flaky"].task_id, TaskStatus.IN_PROGRESS)
        service.update_task_status(tasks["flaky"].task_id, TaskStatus.DONE)
        return tasks

    def test_search_tasks_by_status(self, service, board):
        results = service.search_tasks(TaskFilter(status=TaskStatus.TODO))

        assert results == [board["unit"], board["readme"], board["sprint"]]

    def test_filter_tasks_by_priority(self, service, board):
        results = service.search_tasks(TaskFilter(priority=TaskPriority.MEDIUM))

        assert results == [board["flaky"], board["readme"]]

    def test_search_tasks_by_date_range(self, clock, service, board):
        results = service.search_tasks(
            TaskFilter(due_from=clock.now + timedelta(days=2), due_to=clock.now + timedelta(days=5))
        )

        assert results == [board["integration"], board["unit"]]

    def test_search_tasks_by_partial_title(self, service, board):
        results = service.search_tasks(TaskFilter(title_contains="TESTS"))

        assert results == [board["integration"], board["unit"]]

    def test_search_tasks_combining_filters(self, clock, service, board):
        results = service.search_tasks(
            TaskFilter(status=TaskStatus.TODO, title_contains="write", due_to=clock.now + timedelta(days=4))
        )

        assert results == [board["unit"]]

    def test_search_without_filter_returns_every_task_by_priority(self, service, board):
        results = service.search_tasks()

        assert results == [board["integration"], board["unit"], board["flaky"], board["readme"], board["sprint"]]
