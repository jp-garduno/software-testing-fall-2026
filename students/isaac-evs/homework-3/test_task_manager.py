from src.task_manager import TaskManager


def test_add_task_appends_task():
    manager = TaskManager()
    manager.add_task("Write report")
    assert len(manager.tasks) == 1


def test_remove_task_by_title():
    manager = TaskManager()
    manager.add_task("Write report")
    assert manager.remove_task("Write report") is True
    assert len(manager.tasks) == 0


def test_get_pending_tasks():
    manager = TaskManager()
    manager.add_task("Task 1")
    manager.add_task("Task 2")
    assert len(manager.get_pending_tasks()) == 2


def test_complete_task_marks_done():
    manager = TaskManager()
    manager.add_task("Task 1")
    manager.complete_task("Task 1")
    assert len(manager.get_completed_tasks()) == 1


def test_count_by_priority():
    manager = TaskManager()
    manager.add_task("Task 1", priority="high")
    manager.add_task("Task 2", priority="high")
    manager.add_task("Task 3", priority="low")
    assert manager.count_by_priority("high") == 2


def test_to_json_returns_serialized_tasks():
    manager = TaskManager()
    manager.add_task("Task 1")
    json_output = manager.to_json()
    assert "Task 1" in json_output
