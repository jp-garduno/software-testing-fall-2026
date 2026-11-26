"""Create, complete, delete and edit tasks (Selenium + Page Object Model)."""

import pytest


class TestTaskCreation:
    def test_create_single_task(self, todo_page):
        todo_page.add_todo("Buy milk")
        assert todo_page.get_todo_count() == 1

    def test_create_multiple_tasks_keeps_their_order(self, todo_page):
        todo_page.add_todos("First", "Second", "Third")
        assert todo_page.get_visible_todos() == ["First", "Second", "Third"]

    def test_created_task_appears_in_the_list_as_active(self, todo_page):
        todo_page.add_todo("Buy milk")
        assert todo_page.get_visible_todos() == ["Buy milk"]
        assert not todo_page.is_completed(0)
        assert todo_page.get_items_left() == 1

    def test_input_is_emptied_after_adding(self, todo_page):
        todo_page.add_todo("Buy milk")
        assert todo_page.driver.find_element(*todo_page.NEW_TODO_INPUT).get_attribute("value") == ""

    def test_surrounding_whitespace_is_trimmed(self, todo_page):
        todo_page.add_todo("   spaced out   ")
        assert todo_page.get_visible_todos() == ["spaced out"]

    def test_blank_task_is_not_created(self, todo_page):
        todo_page.add_todo("   ")
        todo_page.add_todo("Real task")  # waits for a row, so the blank one has had its chance to appear
        assert todo_page.get_visible_todos() == ["Real task"]

    def test_markup_is_shown_as_text_not_rendered(self, todo_page):
        todo_page.add_todo('<b>bold</b> & "quotes"')
        assert todo_page.get_visible_todos() == ['<b>bold</b> & "quotes"']

    def test_new_list_starts_empty_without_footer(self, todo_page):
        assert todo_page.get_todo_count() == 0
        assert not todo_page.is_footer_visible()


class TestTaskCompletion:
    def test_mark_task_as_complete(self, todo_page):
        todo_page.add_todo("Read book")
        todo_page.toggle_todo(0)
        assert todo_page.is_completed(0)

    def test_unmark_completed_task(self, todo_page):
        todo_page.add_todo("Read book")
        todo_page.toggle_todo(0)
        todo_page.toggle_todo(0)
        assert not todo_page.is_completed(0)

    def test_complete_multiple_tasks(self, todo_page):
        todo_page.add_todos("One", "Two", "Three")
        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)
        assert [todo_page.is_completed(i) for i in range(3)] == [True, False, True]

    def test_items_left_counter_follows_completion(self, todo_page):
        todo_page.add_todos("One", "Two", "Three")
        todo_page.toggle_todo(1)
        assert todo_page.get_items_left() == 2

    def test_toggle_all_completes_every_task(self, todo_page):
        todo_page.add_todos("One", "Two", "Three")
        todo_page.toggle_all()
        assert all(todo_page.is_completed(i) for i in range(3))
        assert todo_page.get_items_left() == 0

    def test_toggle_all_twice_reopens_every_task(self, todo_page):
        todo_page.add_todos("One", "Two")
        todo_page.toggle_all()
        todo_page.toggle_all()
        assert not any(todo_page.is_completed(i) for i in range(2))


class TestTaskDeletion:
    def test_delete_single_task(self, todo_page):
        todo_page.add_todo("Task to delete")
        todo_page.delete_todo(0)
        assert todo_page.get_todo_count() == 0

    def test_delete_only_the_chosen_task(self, todo_page):
        todo_page.add_todos("Keep A", "Remove me", "Keep B")
        todo_page.delete_todo(1)
        assert todo_page.get_visible_todos() == ["Keep A", "Keep B"]

    def test_delete_completed_task(self, todo_page):
        todo_page.add_todos("Done task", "Open task")
        todo_page.toggle_todo(0)
        todo_page.delete_todo(0)
        assert todo_page.get_visible_todos() == ["Open task"]

    def test_clear_all_completed(self, todo_page):
        todo_page.add_todos("Done 1", "Open", "Done 2")
        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)
        todo_page.clear_completed()
        assert todo_page.get_visible_todos() == ["Open"]

    def test_clear_completed_is_only_offered_when_something_is_completed(self, todo_page):
        todo_page.add_todo("Open")
        assert not todo_page.is_clear_completed_visible()
        todo_page.toggle_todo(0)
        assert todo_page.is_clear_completed_visible()

    def test_footer_disappears_when_the_last_task_is_deleted(self, todo_page):
        todo_page.add_todo("Only task")
        assert todo_page.is_footer_visible()
        todo_page.delete_todo(0)
        assert not todo_page.is_footer_visible()


class TestTaskEditing:
    def test_edit_task_text(self, todo_page):
        todo_page.add_todo("Buy milk")
        todo_page.edit_todo(0, "Buy oat milk")
        assert todo_page.get_visible_todos() == ["Buy oat milk"]

    def test_double_click_opens_the_task_for_editing(self, todo_page):
        todo_page.add_todo("Buy milk")
        todo_page.start_edit(0)
        assert todo_page.is_editing(0)
        assert todo_page.get_edit_value(0) == "Buy milk"

    def test_save_edited_task_by_leaving_the_field(self, todo_page):
        todo_page.add_todos("Buy milk", "Walk dog")
        todo_page.start_edit(1)
        todo_page.type_in_edit(1, "Walk the dog")
        todo_page.blur_edit(1)
        assert todo_page.get_visible_todos() == ["Buy milk", "Walk the dog"]

    def test_edited_text_is_trimmed(self, todo_page):
        todo_page.add_todo("Buy milk")
        todo_page.edit_todo(0, "  Buy bread  ")
        assert todo_page.get_visible_todos() == ["Buy bread"]

    def test_editing_a_task_to_empty_deletes_it(self, todo_page):
        todo_page.add_todos("Keep", "Blank me")
        todo_page.edit_todo(1, "")
        assert todo_page.get_visible_todos() == ["Keep"]

    def test_editing_keeps_the_completed_state(self, todo_page):
        todo_page.add_todo("Buy milk")
        todo_page.toggle_todo(0)
        todo_page.edit_todo(0, "Buy oat milk")
        assert todo_page.is_completed(0)

    @pytest.mark.xfail(
        strict=True,
        reason=(
            "Known defect of this TodoMVC build: the edit field only handles Enter, so Escape does not "
            "cancel (the TodoMVC spec says it should). Strict: this turns red if the app is ever fixed."
        ),
    )
    def test_cancel_edit_with_escape_restores_the_original_text(self, todo_page):
        todo_page.add_todo("Buy milk")
        todo_page.start_edit(0)
        todo_page.type_in_edit(0, "Changed my mind")
        todo_page.cancel_edit(0)
        assert todo_page.wait_until_not_editing(0)
        assert todo_page.get_visible_todos() == ["Buy milk"]
