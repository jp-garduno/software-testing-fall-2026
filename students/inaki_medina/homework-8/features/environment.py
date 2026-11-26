import os

from todo_backends import load_todo_backend


def before_all(context):
    backend_name = os.environ.get("TODO_BACKEND", "selenium")
    context.todo_backend = load_todo_backend(backend_name)


def before_scenario(context, scenario):
    context.todo_page = context.todo_backend.create_todo_page()


def after_scenario(context, scenario):
    todo_page = getattr(context, "todo_page", None)
    if todo_page is not None:
        todo_page.close()