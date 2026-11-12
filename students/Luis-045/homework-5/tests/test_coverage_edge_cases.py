"""Boundaries and regressions identified from the model and service control flow."""

from datetime import timedelta, timezone
from unittest.mock import Mock

import pytest

from src.task import Task, TaskPriority, TaskStatus, as_utc
from src.task_service import TaskService


def test_overdue_check_uses_the_service_clock_for_loaded_tasks(
    service, mock_repository, mock_notification, clock, now
):
    original_clock = Mock(return_value=now)
    task = Task("Loaded task", due_date=now + timedelta(hours=1), clock=original_clock)
    mock_repository.find_all.return_value = [task]
    clock.return_value = now + timedelta(hours=2)
    assert service.check_overdue_tasks() == [task]
    mock_notification.send_email.assert_called_once()


def test_overdue_batch_uses_one_instant_for_all_tasks(
    service, mock_repository, clock, now
):
    tasks = [
        Task(title, due_date=now + timedelta(hours=1), clock=clock)
        for title in ("First task", "Second task")
    ]
    mock_repository.find_all.return_value = tasks
    clock.reset_mock()
    clock.return_value = now + timedelta(hours=2)
    assert service.check_overdue_tasks() == tasks
    clock.assert_called_once_with()


@pytest.mark.parametrize("destination", list(TaskStatus))
def test_archived_tasks_cannot_be_restored_or_rearchived(
    destination, service, mock_repository, clock
):
    task = Task("Archived task", clock=clock)
    task.status = TaskStatus.ARCHIVED
    mock_repository.find_by_id.return_value = task
    with pytest.raises(ValueError, match="Archived"):
        service.update_task_status(task.id, destination)
    mock_repository.save.assert_not_called()


@pytest.mark.parametrize(
    "changes",
    [
        {"title": "ab"},
        {"description": "a" * 501},
        {"description": 42},
        {"priority": 1},
        {"status": "DONE"},
    ],
)
def test_invalid_updated_fields_never_reach_storage(
    changes, service, mock_repository, mock_notification, clock
):
    mock_repository.find_by_id.return_value = Task("Valid task", clock=clock)
    with pytest.raises(ValueError):
        service.update_task("task-id", **changes)
    mock_repository.save.assert_not_called()
    mock_notification.send_email.assert_not_called()


@pytest.mark.parametrize(
    "filters",
    [
        {"status": TaskStatus.DONE},
        {"priority": TaskPriority.HIGH},
        {"title": "missing"},
    ],
)
def test_individual_filters_reject_nonmatching_tasks(
    filters, service, mock_repository, clock
):
    mock_repository.find_all.return_value = [Task("Write tests", clock=clock)]
    assert service.search_tasks(**filters) == []


@pytest.mark.parametrize("filter_name, days", [("start_date", 3), ("end_date", 1)])
def test_date_filters_reject_due_dates_outside_the_range(
    filter_name, days, service, mock_repository, now
):
    mock_repository.find_all.return_value = [
        Task("Scheduled task", due_date=now + timedelta(days=2), clock=lambda: now)
    ]
    assert service.search_tasks(**{filter_name: now + timedelta(days=days)}) == []


@pytest.mark.parametrize("filter_name", ["start_date", "end_date"])
def test_date_filters_reject_nondatetime_values(filter_name, service, mock_repository):
    with pytest.raises(ValueError, match="datetime"):
        service.search_tasks(**{filter_name: "2026-10-20"})
    mock_repository.find_all.assert_not_called()


def test_timezone_offsets_are_normalized_before_comparison(clock, now):
    local_zone = timezone(timedelta(hours=-6))
    local_due = (now + timedelta(hours=1)).astimezone(local_zone)
    task = Task("Timezone task", due_date=local_due, clock=clock)
    assert task.due_date == now + timedelta(hours=1)
    assert task.due_date.tzinfo is timezone.utc


def test_a_naive_clock_is_normalized_to_utc(now):
    task = Task("Naive clock", clock=lambda: now.replace(tzinfo=None))
    assert task.created_at == now
    assert task.created_at.tzinfo is timezone.utc


def test_datetime_normalization_rejects_none():
    with pytest.raises(ValueError, match="datetime"):
        as_utc(None)


def test_clearing_description_is_an_explicit_update(service, mock_repository, clock):
    mock_repository.find_by_id.return_value = Task(
        "Clear description", "Old text", clock=clock
    )
    assert service.update_task("task-id", description=None).description == ""


def test_search_with_empty_title_matches_every_title(service, mock_repository, clock):
    task = Task("Write tests", clock=clock)
    mock_repository.find_all.return_value = [task]
    assert service.search_tasks(title="") == [task]


def test_service_default_clock_sets_utc_creation_time(
    mock_repository, mock_notification
):
    service = TaskService(mock_repository, mock_notification)
    assert service.create_task("Default clock").created_at.tzinfo is timezone.utc
