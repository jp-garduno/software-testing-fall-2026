class TaskRepository:
    """Capa de datos. En los tests siempre se reemplaza por un mock o un fake."""

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
