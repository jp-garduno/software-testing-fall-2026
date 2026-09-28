"""Command-line interface for managing study tasks."""

import argparse
from pathlib import Path

from .storage import load_tasks, save_tasks
from .tasks import add_task, complete_task, pending_tasks, summary


def build_parser() -> argparse.ArgumentParser:
    """Define commands and validate command-line argument types."""
    parser = argparse.ArgumentParser(description="Manage your study tasks.")
    parser.add_argument("--file", type=Path, default=Path("tasks.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    add_parser = commands.add_parser("add", help="Create a task")
    add_parser.add_argument("title")
    add_parser.add_argument("--priority", type=int, choices=(1, 2, 3), default=2)
    done_parser = commands.add_parser("done", help="Complete a task")
    done_parser.add_argument("identifier", type=int)
    list_parser = commands.add_parser("list", help="Display tasks")
    list_parser.add_argument("--pending", action="store_true")
    commands.add_parser("summary", help="Show completion progress")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Execute one command and return a process exit code."""
    parser = build_parser()
    arguments = parser.parse_args(argv)
    try:
        tasks = load_tasks(arguments.file)
        if arguments.command == "add":
            task = add_task(tasks, arguments.title, arguments.priority)
            save_tasks(arguments.file, tasks)
            print(f"Created task {task.identifier}: {task.title}")
        elif arguments.command == "done":
            task = complete_task(tasks, arguments.identifier)
            save_tasks(arguments.file, tasks)
            print(f"Completed task {task.identifier}: {task.title}")
        elif arguments.command == "list":
            visible = pending_tasks(tasks) if arguments.pending else tasks
            if not visible:
                print("No tasks to display.")
            for task in visible:
                marker = "x" if task.completed else " "
                print(
                    f"[{marker}] {task.identifier}: {task.title} "
                    f"(priority {task.priority})"
                )
        else:
            print(summary(tasks))
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
