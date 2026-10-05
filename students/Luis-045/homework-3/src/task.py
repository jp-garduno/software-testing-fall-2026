class Task:
    def __init__(self, title, description="", priority="medium"):
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def update_priority(self, priority):
        allowed = ["low", "medium", "high"]
        if priority not in allowed:
            raise ValueError("Priority must be low, medium, or high")
        self.priority = priority

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
        }

    def __str__(self):
        status = "Done" if self.completed else "Pending"
        return f"{self.title} | {self.priority} | {status}"
