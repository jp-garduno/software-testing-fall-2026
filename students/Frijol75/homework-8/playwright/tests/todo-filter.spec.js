/**
 * Playwright E2E Tests for TodoMVC Filtering Operations (Part 2 - Section 4):
 * 4. Task Filtering (8 points):
 *    - View all tasks
 *    - View active tasks only
 *    - View completed tasks only
 */

const path = require("path");
const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

const SCREENSHOTS_DIR = path.resolve(__dirname, "../../screenshots");

test.describe("4. Task Filtering", () => {
  let todoPage;

  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.navigate();
  });

  test("view all tasks", async () => {
    await todoPage.addTodos(["Active Task 1", "Completed Task 2", "Active Task 3"]);
    await todoPage.toggleTodo(1);

    await todoPage.filterActive();
    expect(await todoPage.getTodoCount()).toBe(2);

    await todoPage.filterAll();
    expect(await todoPage.getTodoCount()).toBe(3);
    expect(await todoPage.getVisibleTodos()).toEqual([
      "Active Task 1",
      "Completed Task 2",
      "Active Task 3",
    ]);
  });

  test("view active tasks only", async () => {
    await todoPage.addTodos(["Write documentation", "Fix bug #42", "Deploy release"]);
    await todoPage.toggleTodo(1);

    await todoPage.filterActive();
    expect(await todoPage.getTodoCount()).toBe(2);
    expect(await todoPage.getVisibleTodos()).toEqual(["Write documentation", "Deploy release"]);
    expect(await todoPage.getActiveCount()).toBe(2);
    await todoPage.takeScreenshot(path.join(SCREENSHOTS_DIR, "playwright_05_filter_active.png"));
  });

  test("view completed tasks only", async () => {
    await todoPage.addTodos(["Morning standup", "Code review", "Update dependencies"]);
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);

    await todoPage.filterCompleted();
    expect(await todoPage.getTodoCount()).toBe(2);
    expect(await todoPage.getVisibleTodos()).toEqual(["Morning standup", "Update dependencies"]);
    expect(await todoPage.getActiveCount()).toBe(1);
    await todoPage.takeScreenshot(path.join(SCREENSHOTS_DIR, "playwright_06_filter_completed.png"));
  });
});

