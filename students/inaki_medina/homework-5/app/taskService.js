// taskService.js

const { Task, TaskPriority } = require("./task");

class TaskService {
  constructor(repository, notificationService) {
    this.repository = repository;
    this.notificationService = notificationService;
  }

  async createTask(
    title,
    description = "",
    priority = TaskPriority.LOW,
    dueDate = null,
  ) {
    const existing = await this.repository.findByTitle(title);
    if (existing) {
      throw new Error(`Task with title '${title}' already exists`);
    }

    const task = new Task(title, description, priority, dueDate);
    await this.repository.save(task);

    await this.notificationService.sendEmail(
      "user@example.com",
      "New Task Created",
      `Task '${title}' has been created`,
    );

    return task;
  }

  async updateTaskStatus(taskId, newStatus) {
    const task = await this.repository.findById(taskId);
    if (!task) {
      throw new Error(`Task ${taskId} not found`);
    }

    if (!task.canTransition(newStatus)) {
      throw new Error(`Invalid transition from ${task.status} to ${newStatus}`);
    }

    const oldStatus = task.status;
    task.status = newStatus;
    task.updatedAt = new Date();

    await this.repository.save(task);

    await this.notificationService.sendEmail(
      "user@example.com",
      "Task Status Updated",
      `Task '${task.title}' changed from ${oldStatus} to ${newStatus}`,
    );

    return task;
  }
}

module.exports = { TaskService };