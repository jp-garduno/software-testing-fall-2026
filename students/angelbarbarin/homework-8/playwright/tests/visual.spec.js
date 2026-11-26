// Bonus A - visual regression.
// Each test brings the app to a key state and compares a screenshot with the baseline in
// tests/__screenshots__/visual.spec.js/. The first run (or --update-snapshots) writes the
// baselines; later runs fail if more than 1% of the pixels differ, and the HTML report
// (npx playwright show-report) shows expected / actual / diff side by side.
const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

let todoPage;

test.beforeEach(async ({ page }) => {
  todoPage = new TodoPage(page);
  await todoPage.navigate();
});

test("empty app", async ({ page }) => {
  await expect(page.locator(".todoapp")).toHaveScreenshot("01-empty.png");
});

test("list with active and completed tasks", async ({ page }) => {
  await todoPage.addTodos("Buy milk", "Walk the dog", "Pay rent");
  await todoPage.toggleTodo(1);

  await expect(page.locator(".todoapp")).toHaveScreenshot("02-mixed-list.png");
});

test("completed filter", async ({ page }) => {
  await todoPage.addTodos("Buy milk", "Walk the dog", "Pay rent");
  await todoPage.toggleTodo(1);
  await todoPage.filterCompleted();

  await expect(page.locator(".todoapp")).toHaveScreenshot("03-completed-filter.png");
});

test("editing a task", async ({ page }) => {
  await todoPage.addTodos("Buy milk", "Walk the dog");
  await todoPage.startEditing(0);

  // The blinking caret would make the screenshot flaky.
  await expect(page.locator(".todoapp")).toHaveScreenshot("04-editing.png", { caret: "hide" });
});

test("all tasks completed", async ({ page }) => {
  await todoPage.addTodos("Buy milk", "Walk the dog");
  await todoPage.toggleAll();

  await expect(page.locator(".todoapp")).toHaveScreenshot("05-all-completed.png");
});
