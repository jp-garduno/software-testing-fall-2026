class TaskRepository:
    """Data access layer (to be mocked in tests)."""

    def __init__(self, database=None):
        self.database = database

    def save(self, task):
        raise NotImplementedError("Must be mocked in tests")

    def find_by_id(self, task_id):
        raise NotImplementedError("Must be mocked in tests")

    def find_by_title(self, title):
        raise NotImplementedError("Must be mocked in tests")

    def find_all(self):
        raise NotImplementedError("Must be mocked in tests")

    def delete(self, task_id):
        raise NotImplementedError("Must be mocked in tests")