const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

let todoPage;

/** Opens an empty app and adds three tasks of which only "Task 2" is completed. */
test.beforeEach(async ({ page }) => {
  todoPage = new TodoPage(page);
  await todoPage.openClean();
});

async function addMixedTodos() {
  await todoPage.addTodos("Task 1", "Task 2", "Task 3");
  await todoPage.toggleTodo(1);
}

test.describe("Filter views", () => {
  test("view all tasks", async () => {
    await addMixedTodos();
    await todoPage.filterAll();
    await expect(todoPage.todoItems).toHaveText(["Task 1", "Task 2", "Task 3"]);
  });

  test("view active tasks only", async () => {
    await addMixedTodos();
    await todoPage.filterActive();
    await expect(todoPage.todoItems).toHaveText(["Task 1", "Task 3"]);
  });

  test("view completed tasks only", async () => {
    await addMixedTodos();
    await todoPage.filterCompleted();
    await expect(todoPage.todoItems).toHaveText(["Task 2"]);
  });

  for (const [name, count] of [
    ["All", 3],
    ["Active", 2],
    ["Completed", 1],
  ]) {
    test(`the ${name} filter shows ${count} task(s)`, async () => {
      await addMixedTodos();
      await todoPage[`filter${name}`]();
      await expect(todoPage.todoItems).toHaveCount(count);
    });
  }

  test("returning to all restores every task", async () => {
    await addMixedTodos();
    await todoPage.filterCompleted();
    await todoPage.filterAll();
    await expect(todoPage.todoItems).toHaveCount(3);
  });

  test("items left counter ignores the filter", async () => {
    await addMixedTodos();
    await todoPage.filterCompleted();
    await expect(todoPage.itemsLeft).toContainText("2 items left");
  });
});

test.describe("Filter behaviour", () => {
  test("all is selected by default", async () => {
    await expect(todoPage.selectedFilter).toHaveText("All");
  });

  test("selecting a filter updates the route", async ({ page }) => {
    await addMixedTodos();
    await todoPage.filterActive();
    await expect(page).toHaveURL(/#\/active$/);
  });

  test("opening a filter route directly applies it", async () => {
    await addMixedTodos();
    await todoPage.navigate("#/completed");
    await expect(todoPage.selectedFilter).toHaveText("Completed");
  });

  test("completing a task in the active view removes it from the view", async () => {
    await addMixedTodos();
    await todoPage.filterActive();
    await todoPage.toggleTodo(0);
    await expect(todoPage.todoItems).toHaveText(["Task 3"]);
  });

  test("reopening a task in the completed view removes it from the view", async () => {
    await addMixedTodos();
    await todoPage.filterCompleted();
    await todoPage.toggleTodo(0);
    await expect(todoPage.todoItems).toHaveCount(0);
  });

  test("clear completed in the all view leaves only active tasks", async () => {
    await addMixedTodos();
    await todoPage.clearCompleted();
    await todoPage.filterCompleted();
    await expect(todoPage.todoItems).toHaveCount(0);
  });
});
