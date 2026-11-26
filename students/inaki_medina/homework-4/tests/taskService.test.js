// taskService.test.js

const { Task, TaskStatus, TaskPriority } = require("../app/task");
const { TaskService } = require("../app/taskService");

describe("TaskService Integration Tests", () => {
  let mockRepository;
  let mockNotificationService;
  let taskService;

  beforeEach(() => {
    mockRepository = {
      save: jest.fn(),
      findById: jest.fn(),
      findByTitle: jest.fn(),
      findAll: jest.fn(),
      deleteById: jest.fn(),
    };

    mockNotificationService = {
      sendEmail: jest.fn(),
      sendSms: jest.fn(),
    };

    taskService = new TaskService(mockRepository, mockNotificationService);
  });

  test("Integration: Creating task saves to repository and sends notification", async () => {
    mockRepository.findByTitle.mockResolvedValue(null);

    const task = await taskService.createTask(
      "Write tests",
      "Unit and integration tests",
      TaskPriority.HIGH,
    );

    expect(task.title).toBe("Write tests");
    expect(mockRepository.save).toHaveBeenCalledWith(task);
    expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(1);
    expect(mockNotificationService.sendEmail.mock.calls[0][1]).toContain(
      "New Task Created",
    );
  });

  test("Integration: Cannot create task with duplicate title", async () => {
    const existingTask = new Task("Existing Task");
    mockRepository.findByTitle.mockResolvedValue(existingTask);

    await expect(taskService.createTask("Existing Task")).rejects.toThrow(
      "already exists",
    );

    expect(mockRepository.save).not.toHaveBeenCalled();
    expect(mockNotificationService.sendEmail).not.toHaveBeenCalled();
  });

  test("Integration: Status update saves and notifies", async () => {
    const task = new Task("Test Task");
    task.status = TaskStatus.TODO;
    mockRepository.findById.mockResolvedValue(task);

    const updatedTask = await taskService.updateTaskStatus(
      1,
      TaskStatus.IN_PROGRESS,
    );

    expect(updatedTask.status).toBe(TaskStatus.IN_PROGRESS);
    expect(mockRepository.save).toHaveBeenCalledTimes(1);
    expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(1);
    expect(mockNotificationService.sendEmail.mock.calls[0][2]).toContain(
      "TODO",
    );
    expect(mockNotificationService.sendEmail.mock.calls[0][2]).toContain(
      "IN_PROGRESS",
    );
  });

  describe("Delete Task", () => {
    test("test_soft_delete_archives_task", async () => {
      const task = new Task("Archive this task");
      mockRepository.findById.mockResolvedValue(task);

      await taskService.softDeleteTask(1);

      expect(task.status).toBe(TaskStatus.ARCHIVED);
      expect(mockRepository.save).toHaveBeenCalledWith(task);
    });

    test("test_archived_task_cannot_be_restored", async () => {
      const task = new Task("Archived task");
      task.status = TaskStatus.ARCHIVED;
      mockRepository.findById.mockResolvedValue(task);

      await expect(
        taskService.updateTaskStatus(1, TaskStatus.TODO),
      ).rejects.toThrow("Invalid transition");

      expect(mockRepository.save).not.toHaveBeenCalled();
    });

    test("test_permanently_deleted_task_is_removed_from_repository", async () => {
      await taskService.permanentlyDeleteTask(1);

      expect(mockRepository.deleteById).toHaveBeenCalledWith(1);
    });
  });

  describe("Overdue Notifications", () => {
    test("test_overdue_task_sends_sms_notification", async () => {
      const task = new Task("Overdue task");
      task.dueDate = new Date(Date.now() - 1000);
      mockRepository.findAll.mockResolvedValue([task]);

      await taskService.notifyOverdueTasks();

      expect(mockNotificationService.sendSms).toHaveBeenCalledTimes(1);
    });

    test("test_overdue_task_triggers_notification", async () => {
      const overdueTask = new Task("Overdue task");
      overdueTask.dueDate = new Date(Date.now() - 1000);
      const futureTask = new Task("Future task");
      futureTask.dueDate = new Date(Date.now() + 24 * 60 * 60 * 1000);
      mockRepository.findAll.mockResolvedValue([overdueTask, futureTask]);

      await taskService.notifyOverdueTasks();

      expect(mockNotificationService.sendSms).toHaveBeenCalledTimes(1);
    });
  });
});