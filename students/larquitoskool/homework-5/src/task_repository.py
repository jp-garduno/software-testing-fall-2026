class TaskRepository:
    def __init__(self, database):
        self.database = database
    def save(self, task): raise NotImplementedError()
    def find_by_id(self, task_id): raise NotImplementedError()
    def find_by_title(self, title): raise NotImplementedError()
    def find_all(self): raise NotImplementedError()
    def delete(self, task_id): raise NotImplementedError()