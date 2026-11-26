"""Pruebas de filtrado de TodoMVC con Selenium + Page Object Model.

Escenario base: 3 tareas -> "Active 1", "Completed 1" (completada), "Active 2".
"""
import pytest


def wait_for_count(page, expected):
    page.wait.until(lambda d: page.get_todo_count() == expected)


@pytest.fixture
def mixed_todos(todo_page):
    """Crea 3 tareas y completa la del medio."""
    for t in ["Active 1", "Completed 1", "Active 2"]:
        todo_page.add_todo(t)
    wait_for_count(todo_page, 3)
    todo_page.toggle_todo(1)
    todo_page.wait.until(lambda d: todo_page.is_completed(1))
    return todo_page


def test_filter_all(mixed_todos):
    page = mixed_todos
    page.filter_active()          # primero nos movemos a otra vista
    wait_for_count(page, 2)

    page.filter_all()

    wait_for_count(page, 3)
    assert page.get_visible_todos() == ["Active 1", "Completed 1", "Active 2"]


def test_filter_active(mixed_todos):
    page = mixed_todos

    page.filter_active()

    wait_for_count(page, 2)
    assert page.get_visible_todos() == ["Active 1", "Active 2"]


def test_filter_completed(mixed_todos):
    page = mixed_todos

    page.filter_completed()

    wait_for_count(page, 1)
    assert page.get_visible_todos() == ["Completed 1"]


def test_filter_persists_via_url(mixed_todos):
    """El filtro se refleja en la URL (#/active), útil como verificación extra."""
    page = mixed_todos

    page.filter_active()

    wait_for_count(page, 2)
    assert page.driver.current_url.endswith("#/active")


def test_completing_task_in_active_view_removes_it(mixed_todos):
    """Caso borde: completar una tarea estando en 'Active' la oculta de la vista."""
    page = mixed_todos
    page.filter_active()
    wait_for_count(page, 2)

    page.toggle_todo(0)

    wait_for_count(page, 1)
    assert page.get_visible_todos() == ["Active 2"]
