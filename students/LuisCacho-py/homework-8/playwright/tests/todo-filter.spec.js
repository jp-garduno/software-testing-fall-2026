const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

test.describe("TodoMVC Task Filtering (Playwright)", () => {
  let todoPage;

  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.navigate();
    await todoPage.addTodos(["Active task 1", "Completed task 2", "Active task 3"]);
    await todoPage.toggleTodo(1);
  });

  test("views all tasks when All filter is selected", async () => {
    await todoPage.filterActive();
    await todoPage.filterAll();
    const todos = await todoPage.getVisibleTodos();
    expect(todos).toHaveLength(3);
    expect(todos).toEqual(["Active task 1", "Completed task 2", "Active task 3"]);
  });

  test("views active tasks only when Active filter is selected", async () => {
    await todoPage.filterActive();
    const todos = await todoPage.getVisibleTodos();
    expect(todos).toHaveLength(2);
    expect(todos).toEqual(["Active task 1", "Active task 3"]);
  });

  test("views completed tasks only when Completed filter is selected", async () => {
    await todoPage.filterCompleted();
    const todos = await todoPage.getVisibleTodos();
    expect(todos).toHaveLength(1);
    expect(todos[0]).toContain("Completed task 2");
  });

  test("clears completed tasks while viewing Completed filter", async () => {
    await todoPage.filterCompleted();
    await todoPage.clearCompleted();
    expect(await todoPage.getTodoCount()).toBe(0);

    await todoPage.filterAll();
    expect(await todoPage.getTodoCount()).toBe(2);
  });
});
