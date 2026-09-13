from src.task_manager import TaskManager


def create_demo_manager():
    manager = TaskManager()
    manager.add_task("Study", "Review static testing notes", "high")
    manager.add_task("Exercise", "Go to the gym", "medium")
    manager.add_task("Homework", "Finish homework 3", "high")
    manager.complete_task("Study")
    return manager


def print_tasks(manager):
    for index, task in enumerate(manager.tasks, start=1):
        print(f"{index}. {task}")


def print_summary(manager):
    print(manager.summary())


def main():
    manager = create_demo_manager()
    print("TODO LIST")
    print_tasks(manager)
    print_summary(manager)


if __name__ == "__main__":
    main()
