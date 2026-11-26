const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

test.describe("Todo filters", () => {
  let todoPage;

  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.navigate();
    await todoPage.addTodo("Active task");
    await todoPage.addTodo("Completed task");
    await todoPage.toggleTodo(1);
  });

  test("shows active and completed todos in All", async ({ page }) => {
    await todoPage.filterAll();

    await expect(page.locator(".todo-list li label")).toHaveText([
      "Active task",
      "Completed task",
    ]);
  });

  test("shows only active todos", async ({ page }) => {
    await todoPage.filterActive();

    await expect(page.locator(".todo-list li label")).toHaveText(["Active task"]);
  });

  test("shows only completed todos", async ({ page }) => {
    await todoPage.filterCompleted();

    await expect(page.locator(".todo-list li label")).toHaveText([
      "Completed task",
    ]);
  });
});
