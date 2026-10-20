"""Database boundary. Inject a database client; tests never contact a database."""


class TaskRepository:
    def __init__(self, database):
        self.database = database

    def save(self, task):
        self.database.save(task)
        return task

    def find_by_id(self, task_id):
        return self.database.find_by_id(task_id)

    def find_all(self):
        return list(self.database.find_all())

    def find_by_title(self, title):
        return next((task for task in self.find_all() if task.title == title), None)

    def delete(self, task_id):
        """Permanent deletion; service.delete_task uses archival instead."""
        self.database.delete(task_id)
