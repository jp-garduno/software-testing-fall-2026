import os

import pytest

from todo_backends import BACKENDS, load_todo_backend


def selected_backends():
    selected_backend = os.environ.get("TODO_BACKEND")
    if selected_backend is None:
        return BACKENDS
    if selected_backend not in BACKENDS:
        raise ValueError(f"Unknown TODO_BACKEND: {selected_backend}")
    return (selected_backend,)


@pytest.fixture(params=selected_backends(), ids=selected_backends())
def todo_page(request):
    backend = load_todo_backend(request.param)
    page = backend.create_todo_page()
    try:
        page.navigate()
        yield page
    finally:
        page.close()
