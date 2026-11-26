const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

test.describe("Todo Management - Filtering", () => {
  let todoPage;

  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.navigate();
    await todoPage.addTodo("Active 1");
    await todoPage.addTodo("Completed 1");
    await todoPage.addTodo("Active 2");
    await todoPage.toggleTodo(1);
  });

  test("view all tasks", async () => {
    await todoPage.filterCompleted();
    await todoPage.filterAll();
    expect(await todoPage.getVisibleTodos()).toEqual([
      "Active 1",
      "Completed 1",
      "Active 2",
    ]);
  });

  test("view active tasks only", async () => {
    await todoPage.filterActive();
    expect(await todoPage.getVisibleTodos()).toEqual(["Active 1", "Active 2"]);
  });

  test("view completed tasks only", async () => {
    await todoPage.filterCompleted();
    expect(await todoPage.getVisibleTodos()).toEqual(["Completed 1"]);
  });
});