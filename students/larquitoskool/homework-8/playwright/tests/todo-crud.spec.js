const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

test.describe("Todo Management - CRUD & Editing", () => {
  let todoPage;

  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.navigate();
  });

  test("create single task", async () => {
    await todoPage.addTodo("Buy milk");
    expect(await todoPage.getTodoCount()).toBe(1);
    expect(await todoPage.getVisibleTodos()).toEqual(["Buy milk"]);
  });

  test("create multiple tasks", async () => {
    const tasks = ["Task 1", "Task 2", "Task 3"];
    for (const task of tasks) {
      await todoPage.addTodo(task);
    }
    expect(await todoPage.getTodoCount()).toBe(3);
    expect(await todoPage.getVisibleTodos()).toEqual(tasks);
  });

  test("mark task as complete and unmark it", async () => {
    await todoPage.addTodo("Write E2E tests");
    await todoPage.toggleTodo(0);
    expect(await todoPage.isTodoCompleted(0)).toBe(true);
    expect(await todoPage.getActiveCount()).toBe(0);

    await todoPage.toggleTodo(0);
    expect(await todoPage.isTodoCompleted(0)).toBe(false);
    expect(await todoPage.getActiveCount()).toBe(1);
  });

  test("complete multiple tasks", async () => {
    await todoPage.addTodo("Task A");
    await todoPage.addTodo("Task B");
    await todoPage.addTodo("Task C");
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);
    expect(await todoPage.isTodoCompleted(0)).toBe(true);
    expect(await todoPage.isTodoCompleted(1)).toBe(false);
    expect(await todoPage.isTodoCompleted(2)).toBe(true);
    expect(await todoPage.getActiveCount()).toBe(1);
  });

  test("delete single task", async () => {
    await todoPage.addTodo("Task to delete");
    await todoPage.deleteTodo(0);
    expect(await todoPage.getTodoCount()).toBe(0);
  });

  test("delete completed task and clear all completed", async () => {
    await todoPage.addTodo("Keep active");
    await todoPage.addTodo("Completed 1");
    await todoPage.addTodo("Completed 2");
    await todoPage.toggleTodo(1);
    await todoPage.toggleTodo(2);

    await todoPage.deleteTodo(1);
    expect(await todoPage.getVisibleTodos()).toEqual(["Keep active", "Completed 2"]);

    await todoPage.clearCompleted();
    expect(await todoPage.getVisibleTodos()).toEqual(["Keep active"]);
  });

  test("edit and save task", async () => {
    await todoPage.addTodo("Initial text");
    await todoPage.editTodo(0, "Updated text", true);
    expect(await todoPage.getVisibleTodos()).toEqual(["Updated text"]);
  });

  test("cancel edit preserves original text", async () => {
    await todoPage.addTodo("Original task");
    await todoPage.editTodo(0, "Should not save", false);
    expect(await todoPage.getVisibleTodos()).toEqual(["Original task"]);
  });
});