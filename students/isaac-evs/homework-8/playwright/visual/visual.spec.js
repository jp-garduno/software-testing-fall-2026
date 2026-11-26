const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

// Visual regression: key states of the app are compared with committed baselines (pixel diff).
// VISUAL_BREAK=1 injects a style change so a run demonstrates how a visual difference is reported.
const SNAPSHOT_OPTIONS = {
  animations: "disabled",
  caret: "hide",
  maxDiffPixelRatio: 0.001,
};

let todoPage;

test.beforeEach(async ({ page }) => {
  todoPage = new TodoPage(page);
  await todoPage.openClean();
  if (process.env.VISUAL_BREAK) {
    await page.addStyleTag({
      content: ".todo-list li.completed label { color: #d00 !important; }",
    });
  }
});

const app = () => todoPage.page.locator(".todoapp");

test("empty list", async () => {
  await expect(app()).toHaveScreenshot("empty-list.png", SNAPSHOT_OPTIONS);
});

test("three tasks, one completed", async () => {
  await todoPage.addTodos("Buy milk", "Walk the dog", "Read a book");
  await todoPage.toggleTodo(1);
  await expect(app()).toHaveScreenshot(
    "three-tasks-one-completed.png",
    SNAPSHOT_OPTIONS,
  );
});

test("active filter", async () => {
  await todoPage.addTodos("Buy milk", "Walk the dog", "Read a book");
  await todoPage.toggleTodo(1);
  await todoPage.filterActive();
  await expect(app()).toHaveScreenshot("active-filter.png", SNAPSHOT_OPTIONS);
});

test("completed filter", async () => {
  await todoPage.addTodos("Buy milk", "Walk the dog", "Read a book");
  await todoPage.toggleTodo(1);
  await todoPage.filterCompleted();
  await expect(app()).toHaveScreenshot(
    "completed-filter.png",
    SNAPSHOT_OPTIONS,
  );
});

test("task in edit mode", async () => {
  await todoPage.addTodos("Buy milk", "Walk the dog");
  await todoPage.startEdit(0);
  await expect(app()).toHaveScreenshot("edit-mode.png", SNAPSHOT_OPTIONS);
});
