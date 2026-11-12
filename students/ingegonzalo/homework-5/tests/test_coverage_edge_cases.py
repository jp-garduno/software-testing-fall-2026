import pytest

from notification_service import NotificationService
from task_repository import TaskRepository


class TestAbstractInterfaces:
    @pytest.mark.parametrize("method,args", [
        ("save", (None,)), ("find_by_id", (1,)), ("find_by_title", ("t",)),
        ("find_all", ()), ("delete", (1,)),
    ])
    def test_repository_methods_must_be_mocked(self, method, args):
        with pytest.raises(NotImplementedError):
            getattr(TaskRepository(database=None), method)(*args)

    @pytest.mark.parametrize("method,args", [
        ("send_email", ("a@b.c", "s", "b")), ("send_sms", ("+52", "msg")),
    ])
    def test_notification_methods_must_be_mocked(self, method, args):
        with pytest.raises(NotImplementedError):
            getattr(NotificationService(), method)(*args)


class TestServiceEdgeCases:
    def test_update_without_arguments_only_touches_updated_at(
            self, task_service, mock_repository, make_task):
        task = make_task("Untouched")
        before = task.updated_at
        mock_repository.find_by_id.return_value = task

        result = task_service.update_task(1)

        assert result.title == "Untouched"
        assert result.updated_at >= before
        mock_repository.find_by_title.assert_not_called()

    def test_update_description_is_truncated(self, task_service, mock_repository, make_task):
        mock_repository.find_by_id.return_value = make_task("Desc task")
        assert len(task_service.update_task(1, description="x" * 900).description) == 500

    def test_update_with_invalid_title_fails(self, task_service, mock_repository, make_task):
        mock_repository.find_by_id.return_value = make_task("Valid title")
        with pytest.raises(ValueError, match="at least 3"):
            task_service.update_task(1, title="ab")

    def test_update_missing_task_fails(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = None
        with pytest.raises(ValueError, match="not found"):
            task_service.update_task(7, title="Whatever")