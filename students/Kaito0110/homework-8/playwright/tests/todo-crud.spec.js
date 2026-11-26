const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

test.describe("Todo CRUD", () => {
  let todoPage;

  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.navigate();
  });

  test("creates and displays a single todo", async () => {
    await todoPage.addTodo("Buy milk");

    await expect(todoPage.todoItems).toHaveCount(1);
    await expect(todoPage.todoItems).toContainText("Buy milk");
  });

  test("creates multiple todos", async () => {
    await todoPage.addTodo("Buy milk");
    await todoPage.addTodo("Read a book");

    await expect(todoPage.todoItems).toHaveCount(2);
    await expect(await todoPage.getVisibleTodos()).toEqual([
      "Buy milk",
      "Read a book",
    ]);
  });

  test("marks a todo complete and incomplete", async () => {
    await todoPage.addTodo("Test completion");
    await todoPage.toggleTodo(0);

    await expect.poll(() => todoPage.isCompleted(0)).toBe(true);
    await expect.poll(() => todoPage.getActiveCount()).toBe(0);

    await todoPage.toggleTodo(0);
    await expect.poll(() => todoPage.isCompleted(0)).toBe(false);
    await expect.poll(() => todoPage.getActiveCount()).toBe(1);
  });

  test("completes multiple todos", async () => {
    await todoPage.addTodo("First task");
    await todoPage.addTodo("Second task");
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(1);

    await expect.poll(() => todoPage.getActiveCount()).toBe(0);
    await expect.poll(() => todoPage.isCompleted(0)).toBe(true);
    await expect.poll(() => todoPage.isCompleted(1)).toBe(true);
  });

  test("deletes a single todo", async () => {
    await todoPage.addTodo("Remove me");
    await todoPage.deleteTodo(0);

    await expect(todoPage.todoItems).toHaveCount(0);
  });

  test("deletes a completed todo", async () => {
    await todoPage.addTodo("Completed task");
    await todoPage.toggleTodo(0);
    await todoPage.deleteTodo(0);

    await expect(todoPage.todoItems).toHaveCount(0);
  });

  test("clears all completed todos", async ({ page }) => {
    await todoPage.addTodo("Completed task");
    await todoPage.addTodo("Active task");
    await todoPage.toggleTodo(0);
    await todoPage.clearCompleted();

    await expect(page.locator(".todo-list li label")).toHaveText(["Active task"]);
  });

  test("edits todo text", async () => {
    await todoPage.addTodo("Original task");
    await todoPage.editTodo(0, "Updated task");

    await expect(todoPage.todoItems.locator("label")).toHaveText(["Updated task"]);
  });

  test("abandons an unchanged todo edit", async () => {
    await todoPage.addTodo("Original task");
    await todoPage.editTodo(0, "Original task", false);

    await expect(todoPage.todoItems.locator("label")).toHaveText([
      "Original task",
    ]);
    await expect(todoPage.todoItems).not.toHaveClass(/editing/);
  });

  test("saves an edited todo", async () => {
    await todoPage.addTodo("Draft");
    await todoPage.editTodo(0, "Saved task");

    await expect(todoPage.todoItems.locator("label")).toHaveText(["Saved task"]);
  });

  test("deletes a todo when its edit is saved empty", async () => {
    await todoPage.addTodo("Remove by empty edit");
    await todoPage.editTodo(0, "");

    await expect(todoPage.todoItems).toHaveCount(0);
  });
});
