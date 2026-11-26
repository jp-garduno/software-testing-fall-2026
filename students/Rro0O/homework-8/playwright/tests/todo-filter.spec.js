/** Filtering tasks by status. */

const { test, expect } = require("./fixtures");

test.describe("Task filtering", () => {
  // Three todos where only the second one is completed.
  test.beforeEach(async ({ todoPage }) => {
    await todoPage.addTodos("Task 1", "Task 2", "Task 3");
    await todoPage.toggleTodo(1);
  });

  test("view all tasks", async ({ todoPage }) => {
    await todoPage.filterActive();

    await todoPage.filterAll();

    await expect(todoPage.itemLabels).toHaveText(["Task 1", "Task 2", "Task 3"]);
    await expect(todoPage.selectedFilter).toHaveText("All");
  });

  test("view active tasks only", async ({ todoPage }) => {
    await todoPage.filterActive();

    await expect(todoPage.itemLabels).toHaveText(["Task 1", "Task 3"]);
    await expect(todoPage.selectedFilter).toHaveText("Active");
  });

  test("view completed tasks only", async ({ todoPage }) => {
    await todoPage.filterCompleted();

    await expect(todoPage.itemLabels).toHaveText(["Task 2"]);
    await expect(todoPage.selectedFilter).toHaveText("Completed");
  });

  test("completing task under active filter hides it", async ({ todoPage }) => {
    await todoPage.filterActive();

    await todoPage.toggleTodo(0);

    await expect(todoPage.itemLabels).toHaveText(["Task 3"]);
    await expect(todoPage.counter).toHaveText("1 item left!");
  });
});
