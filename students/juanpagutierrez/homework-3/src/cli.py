"""Command-line entry point for the task manager."""

import argparse

from storage import get_storage_summary
from task_manager import TaskManager


def build_parser():
    """Build and return the argparse parser for the CLI."""
    parser = argparse.ArgumentParser(description="Simple Task Manager CLI")
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add")
    add_p.add_argument("title")
    add_p.add_argument("--priority", default="medium")

    done_p = sub.add_parser("done")
    done_p.add_argument("task_id", type=int)

    remove_p = sub.add_parser("remove")
    remove_p.add_argument("task_id", type=int)

    sub.add_parser("list")
    sub.add_parser("summary")

    return parser


def main():
    """Parse CLI arguments and dispatch to the TaskManager."""
    parser = build_parser()
    args = parser.parse_args()
    manager = TaskManager()

    if args.command == "add":
        task = manager.add_task(args.title, args.priority)
        print(f"Added task #{task['id']}: {task['title']}")
    elif args.command == "done":
        ok = manager.complete_task(args.task_id)
        print("Marked as done" if ok else "Task not found")
    elif args.command == "remove":
        ok = manager.remove_task(args.task_id)
        print("Removed" if ok else "Task not found")
    elif args.command == "list":
        for task in manager.list_tasks():
            status = "x" if task["completed"] else " "
            print(f"[{status}] #{task['id']} ({task['priority']}) {task['title']}")
    elif args.command == "summary":
        summary = get_storage_summary(manager.tasks)
        print(summary)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
