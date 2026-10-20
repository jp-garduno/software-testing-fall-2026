
// task.test.js

const { Task, TaskStatus, TaskPriority } = require("../app/task");

describe("Task Creation", () => {
  test("Unit test: Create task with valid data", () => {
    const dueDate = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
    const task = new Task(
      "Write unit tests",
      "Complete homework 5",
      TaskPriority.HIGH,
      dueDate,
    );

    expect(task.title).toBe("Write unit tests");
    expect(task.description).toBe("Complete homework 5");
    expect(task.status).toBe(TaskStatus.TODO);
    expect(task.priority).toBe(TaskPriority.HIGH);
    expect(task.dueDate).toBe(dueDate);
  });

  test("Unit test: Reject title with fewer than 3 characters", () => {
    expect(() => new Task("ab")).toThrow("at least 3 characters");
  });

  test("Unit test: Reject title exceeding 100 characters", () => {
    const longTitle = "a".repeat(101);
    expect(() => new Task(longTitle)).toThrow("not exceed 100 characters");
  });
});

describe("Status Transitions", () => {
  test("Unit test: Valid transition from TODO to IN_PROGRESS", () => {
    const task = new Task("Test task");
    expect(task.canTransition(TaskStatus.IN_PROGRESS)).toBe(true);
  });

  test("Unit test: Invalid backward transition", () => {
    const task = new Task("Test task");
    task.status = TaskStatus.DONE;
    expect(task.canTransition(TaskStatus.IN_PROGRESS)).toBe(false);
  });
});

describe("Overdue Detection", () => {
  test("Unit test: Detect an overdue unfinished task", () => {
    const task = new Task("Overdue task");
    task.dueDate = new Date(Date.now() - 1000);

    expect(task.isOverdue()).toBe(true);
  });

  test("Unit test: Completed and archived tasks are not overdue", () => {
    const task = new Task("Finished task");
    task.dueDate = new Date(Date.now() - 1000);

    task.status = TaskStatus.DONE;
    expect(task.isOverdue()).toBe(false);

    task.status = TaskStatus.ARCHIVED;
    expect(task.isOverdue()).toBe(false);
  });
});

describe("Priority Comparison", () => {
  test("Unit test: Compare higher, lower, and equal priorities", () => {
    const highPriorityTask = new Task("High task", "", TaskPriority.HIGH);
    const lowPriorityTask = new Task("Low task", "", TaskPriority.LOW);
    const anotherHighPriorityTask = new Task(
      "Another high task",
      "",
      TaskPriority.HIGH,
    );

    expect(highPriorityTask.comparePriority(lowPriorityTask)).toBe(1);
    expect(lowPriorityTask.comparePriority(highPriorityTask)).toBe(-1);
    expect(highPriorityTask.comparePriority(anotherHighPriorityTask)).toBe(0);
  });
});

describe("Due Date Validation", () => {
  test("Unit test: Accept a future dueDate", () => {
    const task = new Task("Future due date task");
    const futureDueDate = new Date(Date.now() + 24 * 60 * 60 * 1000);

    expect(() => task.validateDueDate(futureDueDate)).not.toThrow();
  });

  test("Unit test: Reject a past dueDate", () => {
    const task = new Task("Past due date task");
    const pastDueDate = new Date(Date.now() - 24 * 60 * 60 * 1000);

    expect(() => task.validateDueDate(pastDueDate)).toThrow(
      "Due date must be in the future",
    );
  });
});