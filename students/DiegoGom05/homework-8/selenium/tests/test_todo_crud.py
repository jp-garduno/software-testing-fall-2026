"""Pruebas CRUD de TodoMVC con Selenium + Page Object Model.

Cubre: creación, completado, borrado y edición de tareas.
Cada test usa la fixture `todo_page` (conftest.py), que abre un
navegador limpio, por lo que los tests son independientes.
"""
import pytest

# ---------------------------------------------------------------- helpers
def wait_for_count(page, expected):
    """Espera explícita hasta que haya `expected` tareas en la lista."""
    page.wait.until(lambda d: page.get_todo_count() == expected)


def wait_for_completed(page, index, expected=True):
    """Espera explícita hasta que la tarea `index` tenga el estado dado."""
    page.wait.until(lambda d: page.is_completed(index) == expected)


# ------------------------------------------------- 1. Creación de tareas
def test_create_single_task(todo_page):
    todo_page.add_todo("Buy milk")

    wait_for_count(todo_page, 1)
    assert todo_page.get_visible_todos() == ["Buy milk"]


def test_create_multiple_tasks(todo_page):
    tasks = ["Task A", "Task B", "Task C"]
    for t in tasks:
        todo_page.add_todo(t)

    wait_for_count(todo_page, 3)
    assert todo_page.get_visible_todos() == tasks


def test_task_appears_in_list(todo_page):
    todo_page.add_todo("Visible task")

    wait_for_count(todo_page, 1)
    assert "Visible task" in todo_page.get_visible_todos()


def test_empty_task_is_not_created(todo_page):
    """Caso borde: Enter con el campo vacío no crea nada."""
    todo_page.add_todo("")

    assert todo_page.get_todo_count() == 0


# ----------------------------------------------- 2. Completado de tareas
def test_complete_task(todo_page):
    todo_page.add_todo("Finish homework")
    wait_for_count(todo_page, 1)

    todo_page.toggle_todo(0)

    wait_for_completed(todo_page, 0, True)
    assert todo_page.is_completed(0)


def test_uncomplete_task(todo_page):
    todo_page.add_todo("Toggle me")
    wait_for_count(todo_page, 1)
    todo_page.toggle_todo(0)
    wait_for_completed(todo_page, 0, True)

    todo_page.toggle_todo(0)

    wait_for_completed(todo_page, 0, False)
    assert not todo_page.is_completed(0)


def test_complete_multiple_tasks(todo_page):
    for t in ["One", "Two", "Three"]:
        todo_page.add_todo(t)
    wait_for_count(todo_page, 3)

    todo_page.toggle_todo(0)
    todo_page.toggle_todo(2)

    wait_for_completed(todo_page, 0, True)
    wait_for_completed(todo_page, 2, True)
    assert todo_page.is_completed(0)
    assert not todo_page.is_completed(1)  # la del medio sigue activa
    assert todo_page.is_completed(2)


# ------------------------------------------------- 3. Borrado de tareas
def test_delete_single_task(todo_page):
    todo_page.add_todo("Task to delete")
    wait_for_count(todo_page, 1)

    todo_page.delete_todo(0)

    wait_for_count(todo_page, 0)
    assert todo_page.get_visible_todos() == []


def test_delete_completed_task(todo_page):
    todo_page.add_todo("Done task")
    todo_page.add_todo("Pending task")
    wait_for_count(todo_page, 2)
    todo_page.toggle_todo(0)
    wait_for_completed(todo_page, 0, True)

    todo_page.delete_todo(0)

    wait_for_count(todo_page, 1)
    assert todo_page.get_visible_todos() == ["Pending task"]


def test_clear_all_completed(todo_page):
    for t in ["A", "B", "C"]:
        todo_page.add_todo(t)
    wait_for_count(todo_page, 3)
    todo_page.toggle_todo(0)
    todo_page.toggle_todo(1)
    wait_for_completed(todo_page, 1, True)

    todo_page.clear_completed()

    wait_for_count(todo_page, 1)
    assert todo_page.get_visible_todos() == ["C"]


# -------------------------------------------------- 4. Edición de tareas
def test_edit_task_text(todo_page):
    todo_page.add_todo("Old text")
    wait_for_count(todo_page, 1)

    todo_page.edit_todo(0, "New text", commit=True)

    todo_page.wait.until(lambda d: todo_page.get_visible_todos() == ["New text"])
    assert todo_page.get_visible_todos() == ["New text"]


@pytest.mark.xfail(
    reason="En esta versión de TodoMVC, Escape no sale del modo edición",
    strict=False,
)
def test_cancel_edit(todo_page):
    todo_page.add_todo("Original")
    wait_for_count(todo_page, 1)

    todo_page.edit_todo(0, "Changed", commit=False)  # Escape

    todo_page.wait.until(lambda d: todo_page.get_visible_todos() == ["Original"])
    assert todo_page.get_visible_todos() == ["Original"]

def test_save_edited_task_persists_after_other_actions(todo_page):
    """Guardar con Enter y comprobar que el cambio sobrevive a otra acción."""
    todo_page.add_todo("Edit me")
    todo_page.add_todo("Other")
    wait_for_count(todo_page, 2)

    todo_page.edit_todo(0, "Edited", commit=True)
    todo_page.toggle_todo(1)  # otra acción cualquiera
    wait_for_completed(todo_page, 1, True)

    assert todo_page.get_visible_todos() == ["Edited", "Other"]


def test_edit_to_empty_deletes_task(todo_page):
    """Caso borde: dejar el texto vacío y confirmar elimina la tarea."""
    todo_page.add_todo("Soon gone")
    wait_for_count(todo_page, 1)

    todo_page.edit_todo(0, "", commit=True)

    wait_for_count(todo_page, 0)
