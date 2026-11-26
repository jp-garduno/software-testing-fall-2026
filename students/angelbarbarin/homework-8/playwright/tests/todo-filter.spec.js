// Playwright end-to-end tests: All / Active / Completed filters.
// Same scenarios as selenium/tests/test_todo_filter.py.
const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

let todoPage;

// Three todos, the middle one completed.
test.beforeEach(async ({ page }) => {
  todoPage = new TodoPage(page);
  await todoPage.navigate();
  await todoPage.addTodos("Task 1", "Task 2", "Task 3");
  await todoPage.toggleTodo(1);
});

test("view all tasks", async () => {
  await todoPage.filterAll();

  await expect(todoPage.todoItems).toHaveText(["Task 1", "Task 2", "Task 3"]);
  await expect(todoPage.filterLink("All")).toHaveClass(/selected/);
});

test("view active tasks only", async ({ page }) => {
  await todoPage.filterActive();

  await expect(todoPage.todoItems).toHaveText(["Task 1", "Task 3"]);
  await expect(page).toHaveURL(/#\/active$/);
});

test("view completed tasks only", async ({ page }) => {
  await todoPage.filterCompleted();

  await expect(todoPage.todoItems).toHaveText(["Task 2"]);
  await expect(page).toHaveURL(/#\/completed$/);
});

test("all is selected by default", async () => {
  await expect(todoPage.filterLink("All")).toHaveClass(/selected/);
  await expect(todoPage.filterLink("Active")).not.toHaveClass(/selected/);
});

test("completing task in active view removes it", async () => {
  await todoPage.filterActive();

  await todoPage.toggleTodo(0);

  await expect(todoPage.todoItems).toHaveText(["Task 3"]);
});

test("new task in completed view is not shown", async () => {
  await todoPage.filterCompleted();

  await todoPage.addTodo("Task 4");

  await expect(todoPage.todoItems).toHaveText(["Task 2"]);
  await todoPage.filterAll();
  await expect(todoPage.todoItems).toHaveCount(4);
});

test("clear completed from completed view empties it", async () => {
  await todoPage.filterCompleted();

  await todoPage.clearCompleted();

  await expect(todoPage.todoItems).toHaveCount(0);
  await todoPage.filterAll();
  await expect(todoPage.todoItems).toHaveText(["Task 1", "Task 3"]);
});

const cases = [
  { filter: "All", expected: ["Task 1", "Task 2", "Task 3"] },
  { filter: "Active", expected: ["Task 1", "Task 3"] },
  { filter: "Completed", expected: ["Task 2"] },
];
for (const { filter, expected } of cases) {
  test(`filter by name: ${filter}`, async () => {
    await todoPage.filterBy(filter);

    await expect(todoPage.todoItems).toHaveText(expected);
  });
}

test("unknown filter name is rejected", async () => {
  await expect(todoPage.filterBy("Archived")).rejects.toThrow("Unknown filter");
});
