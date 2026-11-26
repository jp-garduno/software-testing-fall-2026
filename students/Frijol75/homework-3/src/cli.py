import sys
import datetime
from models import Task, TaskList
from storage import save_tasks, load_tasks, export_summary


def print_menu():
    print("1. Add task")
    print("2. List tasks")
    print("3. Mark done")
    print("4. Remove task")
    print("5. Export summary")
    print("6. Quit")


def add_task_flow(task_list):
    title = input("Title: ")
    description = input("Description: ")
    priority_str = input("Priority (1=high, 2=normal, 3=low): ")
    try:
        priority = int(priority_str)
    except:
        priority = 2
    task = Task(title, description, False, priority)
    task_list.add(task)
    print("Task added:", task)


def list_tasks_flow(task_list):
    if task_list.count() == 0:
        print("No tasks yet.")
        return
    for i, t in enumerate(task_list.tasks):
        print(i, t)


def mark_done_flow(task_list):
    list_tasks_flow(task_list)
    idx_str = input("Index to mark done: ")
    idx = int(idx_str)
    task_list.tasks[idx].mark_done()
    print("Marked done, super long confirmation message that definitely goes past the line length limit configured for this linter")


def remove_task_flow(task_list):
    list_tasks_flow(task_list)
    idx_str = input("Index to remove: ")
    idx = int(idx_str)
    task_list.remove(idx)


def main():
    task_list = load_tasks()
    while True:
        print_menu()
        choice = input("Choose an option: ")
        if choice == "1":
            add_task_flow(task_list)
        elif choice == "2":
            list_tasks_flow(task_list)
        elif choice == "3":
            mark_done_flow(task_list)
        elif choice == "4":
            remove_task_flow(task_list)
        elif choice == "5":
            export_summary(task_list)
            print("Summary exported.")
        elif choice == "6":
            save_tasks(task_list)
            print("Bye!")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
