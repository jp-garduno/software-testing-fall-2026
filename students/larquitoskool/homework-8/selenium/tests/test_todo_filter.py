class TestTaskFiltering:
    def _seed_tasks(self, todo_page):
        todo_page.add_todo("Active 1")
        todo_page.add_todo("Completed 1")
        todo_page.add_todo("Active 2")
        todo_page.toggle_todo(1)

    def test_view_all_tasks(self, todo_page):
        self._seed_tasks(todo_page)
        todo_page.filter_completed()
        todo_page.filter_all()
        assert todo_page.get_visible_todos() == ["Active 1", "Completed 1", "Active 2"]

    def test_view_active_tasks_only(self, todo_page):
        self._seed_tasks(todo_page)
        todo_page.filter_active()
        assert todo_page.get_visible_todos() == ["Active 1", "Active 2"]

    def test_view_completed_tasks_only(self, todo_page):
        self._seed_tasks(todo_page)
        todo_page.filter_completed()
        assert todo_page.get_visible_todos() == ["Completed 1"]