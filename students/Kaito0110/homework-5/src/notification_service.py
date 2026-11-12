
class NotificationService:
    def __init__(self):
        self.sent_notifications = []

    def send_task_created(self, task):
        message = f"Task created: {task.title}"
        self.sent_notifications.append(message)
        return message

    def send_task_completed(self, task):
        message = f"Task completed: {task.title}"
        self.sent_notifications.append(message)
        return message
