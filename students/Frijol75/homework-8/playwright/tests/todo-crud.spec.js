/**
 * Playwright E2E Tests for TodoMVC CRUD Operations (Part 2):
 * 1. Task Creation (single, multiple, list verification)
 * 2. Task Completion (mark complete, unmark completed, complete multiple)
 * 3. Task Deletion (delete single, delete completed, clear all completed)
 * 5. Task Editing (edit task text, cancel edit, save edited task)
 */

const path = require("path");
const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

const SCREENSHOTS_DIR = path.resolve(__dirname, "../../screenshots");

test.describe("TodoMVC CRUD Operations", () => {
  let todoPage;

  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.navigate();
  });

  test.describe("1. Task Creation", () => {
    test("create single task", async () => {
      await todoPage.addTodo("Buy groceries");
      expect(await todoPage.getTodoCount()).toBe(1);
      expect(await todoPage.getVisibleTodos()).toEqual(["Buy groceries"]);
      expect(await todoPage.getActiveCount()).toBe(1);
      await todoPage.takeScreenshot(path.join(SCREENSHOTS_DIR, "playwright_01_single_task.png"));
    });

    test("create multiple tasks", async () => {
      const tasks = ["Write Playwright tests", "Implement Page Object Model", "Run E2E suite"];
      await todoPage.addTodos(tasks);
      expect(await todoPage.getTodoCount()).toBe(3);
      expect(await todoPage.getVisibleTodos()).toEqual(tasks);
      expect(await todoPage.getActiveCount()).toBe(3);
      await todoPage.takeScreenshot(path.join(SCREENSHOTS_DIR, "playwright_02_multiple_tasks.png"));
    });

    test("task appears in list immediately as active", async () => {
      await todoPage.addTodo("Review pull request");
      const visible = await todoPage.getVisibleTodos();
      expect(visible).toContain("Review pull request");
      expect(await todoPage.isTodoCompleted(0)).toBe(false);
    });
  });

  test.describe("2. Task Completion", () => {
    test("mark task as complete", async () => {
      await todoPage.addTodo("Finish homework 8");
      expect(await todoPage.isTodoCompleted(0)).toBe(false);

      await todoPage.toggleTodo(0);
      expect(await todoPage.isTodoCompleted(0)).toBe(true);
      expect(await todoPage.getActiveCount()).toBe(0);
      await todoPage.takeScreenshot(path.join(SCREENSHOTS_DIR, "playwright_03_task_completed.png"));
    });

    test("unmark completed task", async () => {
      await todoPage.addTodo("Pay electricity bill");
      await todoPage.toggleTodo(0);
      expect(await todoPage.isTodoCompleted(0)).toBe(true);

      await todoPage.toggleTodo(0);
      expect(await todoPage.isTodoCompleted(0)).toBe(false);
      expect(await todoPage.getActiveCount()).toBe(1);
    });

    test("complete multiple tasks", async () => {
      await todoPage.addTodos(["Task A", "Task B", "Task C"]);
      await todoPage.toggleTodo(0);
      await todoPage.toggleTodo(2);

      expect(await todoPage.isTodoCompleted(0)).toBe(true);
      expect(await todoPage.isTodoCompleted(1)).toBe(false);
      expect(await todoPage.isTodoCompleted(2)).toBe(true);
      expect(await todoPage.getActiveCount()).toBe(1);
    });
  });

  test.describe("3. Task Deletion", () => {
    test("delete single task", async () => {
      await todoPage.addTodo("Temporary task");
      expect(await todoPage.getTodoCount()).toBe(1);

      await todoPage.deleteTodo(0);
      expect(await todoPage.getTodoCount()).toBe(0);
    });

    test("delete completed task", async () => {
      await todoPage.addTodos(["Keep me", "Delete me when done"]);
      await todoPage.toggleTodo(1);
      expect(await todoPage.isTodoCompleted(1)).toBe(true);

      await todoPage.deleteTodo(1);
      expect(await todoPage.getTodoCount()).toBe(1);
      expect(await todoPage.getVisibleTodos()).toEqual(["Keep me"]);
    });

    test("clear all completed tasks", async () => {
      await todoPage.addTodos(["Task 1", "Task 2", "Task 3"]);
      await todoPage.toggleTodo(0);
      await todoPage.toggleTodo(1);

      await todoPage.clearCompleted();
      expect(await todoPage.getTodoCount()).toBe(1);
      expect(await todoPage.getVisibleTodos()).toEqual(["Task 3"]);
    });
  });

  test.describe("5. Task Editing", () => {
    test("edit task text", async () => {
      await todoPage.addTodo("Initial draft");
      await todoPage.editTodo(0, "Updated final version");

      expect(await todoPage.getTodoCount()).toBe(1);
      expect(await todoPage.getVisibleTodos()).toEqual(["Updated final version"]);
      await todoPage.takeScreenshot(path.join(SCREENSHOTS_DIR, "playwright_04_task_edited.png"));
    });

    test("cancel edit", async () => {
      await todoPage.addTodo("Original task title");
      await todoPage.cancelEditTodo(0, "Discarded change");

      expect(await todoPage.getTodoCount()).toBe(1);
      expect(await todoPage.getVisibleTodos()).toEqual(["Original task title"]);
    });

    test("save edited task among multiple items", async () => {
      await todoPage.addTodos(["First item", "Second item", "Third item"]);
      await todoPage.editTodo(1, "Second item (Edited)");

      expect(await todoPage.getVisibleTodos()).toEqual([
        "First item",
        "Second item (Edited)",
        "Third item",
      ]);
    });
  });
});

