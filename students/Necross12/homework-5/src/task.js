const TaskStatus = {
    TODO: "TODO",
    IN_PROGRESS: "IN_PROGRESS",
    DONE: "DONE",
    ARCHIVED: "ARCHIVED",
};

const TaskPriority = {
    LOW: 1,
    MEDIUM: 2,
    HIGH: 3,
    URGENT: 4,
};

class Task {
    constructor(
        title,
        description = "",
        priority = TaskPriority.LOW,
        dueDate = null,
    )
    {
        Task.validateTitle(title);
        this.title = title;
        this.description = description.substring(0, 500);
        this.status = TaskStatus.TODO;
        this.priority = priority;
        this.dueDate = dueDate;
        this.createdAt = new Date();
        this.updatedAt = new Date();

        if (dueDate)
            this.validateDueDate(dueDate);
    }

    static validateTitle(title) {
        if (!title || title.length < 3)
            throw new Error("Title must be at least 3 characters");
        if (title.length > 100)
            throw new Error("Title must not exceed 100 characters");
    }

    validateDueDate(dueDate) {
        if (dueDate < new Date())
            throw new Error("Due date must be in the future");
    }

    canTransition(newStatus) {
        if (this.status === TaskStatus.ARCHIVED)
            return false;
        if (newStatus === TaskStatus.ARCHIVED)
            return true;

        const transitions = {
            [TaskStatus.TODO]: [TaskStatus.IN_PROGRESS],
            [TaskStatus.IN_PROGRESS]: [TaskStatus.DONE],
            [TaskStatus.DONE]: [],
        };

        return (transitions[this.status] || []).includes(newStatus);
    }

    isOverdue() {
        if (this.status === TaskStatus.DONE || this.status === TaskStatus.ARCHIVED)
            return false;
        if (!this.dueDate)
            return false;
        return new Date() > this.dueDate;
    }

    comparePriority(otherTask) {
        if (this.priority > otherTask.priority)
            return 1;
        if (this.priority < otherTask.priority)
            return -1;
        return 0;
    }
}

module.exports = {
    Task,
    TaskStatus,
    TaskPriority
};
