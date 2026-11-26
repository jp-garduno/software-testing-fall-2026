const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

test.describe("TodoMVC CRUD Operations (Playwright)", () => {
  let todoPage;

  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.navigate();
  });

  // 1. Task Creation
  test("creates a single task and displays it in the list", async () => {
    await todoPage.addTodo("Buy milk");
    expect(await todoPage.getTodoCount()).toBe(1);
    expect(await todoPage.getVisibleTodos()).toContain("Buy milk");
    expect(await todoPage.getActiveCount()).toBe(1);
  });

  test("creates multiple tasks in order", async () => {
    const tasks = ["Write Selenium POM", "Write Playwright POM", "Write BDD Feature"];
    await todoPage.addTodos(tasks);
    expect(await todoPage.getTodoCount()).toBe(3);
    expect(await todoPage.getVisibleTodos()).toEqual(tasks);
  });

  // 2. Task Completion
  test("marks a task as complete and updates active counter", async () => {
    await todoPage.addTodo("Test task");
    await todoPage.toggleTodo(0);
    expect(await todoPage.isTodoCompleted(0)).toBe(true);
    expect(await todoPage.getActiveCount()).toBe(0);
  });

  test("unmarks a completed task back to active", async () => {
    await todoPage.addTodo("Review code");
    await todoPage.toggleTodo(0);
    expect(await todoPage.isTodoCompleted(0)).toBe(true);
    await todoPage.toggleTodo(0);
    expect(await todoPage.isTodoCompleted(0)).toBe(false);
    expect(await todoPage.getActiveCount()).toBe(1);
  });

  test("completes multiple tasks and toggles all", async () => {
    await todoPage.addTodos(["Task 1", "Task 2", "Task 3"]);
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);
    expect(await todoPage.getActiveCount()).toBe(1);

    await todoPage.toggleAll();
    expect(await todoPage.getActiveCount()).toBe(0);
  });

  // 3. Task Deletion
  test("deletes a single active task", async () => {
    await todoPage.addTodo("Task to delete");
    await todoPage.deleteTodo(0);
    expect(await todoPage.getTodoCount()).toBe(0);
  });

  test("deletes a completed task and clears completed items", async () => {
    await todoPage.addTodos(["Completed 1", "Active 2", "Completed 3"]);
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);
    await todoPage.deleteTodo(0);
    expect(await todoPage.getTodoCount()).toBe(2);

    await todoPage.clearCompleted();
    expect(await todoPage.getTodoCount()).toBe(1);
    expect(await todoPage.getVisibleTodos()).toEqual(["Active 2"]);
  });

  // 5. Task Editing
  test("edits task text and saves on Enter", async () => {
    await todoPage.addTodo("Initial title");
    await todoPage.editTodo(0, "Updated title");
    expect(await todoPage.getVisibleTodos()).toEqual(["Updated title"]);
  });

  test("cancels task edit on Escape key", async () => {
    await todoPage.addTodo("Permanent title");
    await todoPage.cancelEditTodo(0, "Temporary title");
    expect(await todoPage.getVisibleTodos()).toEqual(["Permanent title"]);
  });
});
