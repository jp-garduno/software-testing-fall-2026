// Playwright end-to-end tests: creating, completing, deleting and editing todos.
// Same scenarios as selenium/tests/test_todo_crud.py. Assertions use web-first matchers
// (toHaveText, toHaveCount...) that retry until they pass or time out.
const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

let todoPage;

test.beforeEach(async ({ page }) => {
  todoPage = new TodoPage(page);
  await todoPage.navigate();
});

test.describe("Task creation", () => {
  test("create single task", async () => {
    await todoPage.addTodo("Buy milk");

    await expect(todoPage.todoItems).toHaveText(["Buy milk"]);
  });

  test("create multiple tasks keeps order", async () => {
    await todoPage.addTodos("Buy milk", "Walk the dog", "Pay rent");

    await expect(todoPage.todoItems).toHaveText(["Buy milk", "Walk the dog", "Pay rent"]);
    await expect(todoPage.todoCount).toHaveText("3 items left!");
  });

  test("new task appears in list and clears input", async () => {
    await todoPage.addTodo("Read chapter 8");

    expect(await todoPage.getVisibleTodos()).toContain("Read chapter 8");
    await expect(todoPage.newTodoInput).toHaveValue("");
    await expect(todoPage.footer).toBeVisible();
  });

  test("blank task is ignored", async () => {
    await todoPage.addTodo("   ");

    await expect(todoPage.todoItems).toHaveCount(0);
    await expect(todoPage.footer).toBeHidden();
  });

  test("task text is trimmed", async () => {
    await todoPage.addTodo("   Call mom   ");

    await expect(todoPage.todoItems).toHaveText(["Call mom"]);
  });
});

test.describe("Task completion", () => {
  test("mark task as complete", async () => {
    await todoPage.addTodo("Write report");

    await todoPage.toggleTodo(0);

    await expect(todoPage.item(0)).toHaveClass(/completed/);
    await expect(todoPage.todoCount).toHaveText("0 items left!");
  });

  test("unmark completed task", async () => {
    await todoPage.addTodo("Write report");
    await todoPage.toggleTodo(0);

    await todoPage.toggleTodo(0);

    await expect(todoPage.item(0)).not.toHaveClass(/completed/);
    await expect(todoPage.todoCount).toHaveText("1 item left!");
  });

  test("complete multiple tasks", async () => {
    await todoPage.addTodos("Task A", "Task B", "Task C");

    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);

    await expect(todoPage.item(0)).toHaveClass(/completed/);
    await expect(todoPage.item(1)).not.toHaveClass(/completed/);
    await expect(todoPage.item(2)).toHaveClass(/completed/);
    await expect(todoPage.todoCount).toHaveText("1 item left!");
  });

  test("toggle all completes every task", async () => {
    await todoPage.addTodos("Task A", "Task B");

    await todoPage.toggleAll();

    await expect(todoPage.todoItems).toHaveClass([/completed/, /completed/]);
    await expect(todoPage.todoCount).toHaveText("0 items left!");
  });
});

test.describe("Task deletion", () => {
  test("delete single task", async () => {
    await todoPage.addTodos("Keep me", "Delete me");

    await todoPage.deleteTodo(1);

    await expect(todoPage.todoItems).toHaveText(["Keep me"]);
  });

  test("delete completed task", async () => {
    await todoPage.addTodos("Done task", "Pending task");
    await todoPage.toggleTodo(0);

    await todoPage.deleteTodo(0);

    await expect(todoPage.todoItems).toHaveText(["Pending task"]);
    await expect(todoPage.todoCount).toHaveText("1 item left!");
  });

  test("clear all completed", async () => {
    await todoPage.addTodos("Done 1", "Pending", "Done 2");
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);

    await todoPage.clearCompleted();

    await expect(todoPage.todoItems).toHaveText(["Pending"]);
    await expect(todoPage.clearCompletedButton).toBeHidden();
  });

  test("deleting last task hides footer", async () => {
    await todoPage.addTodo("Only task");

    await todoPage.deleteTodo(0);

    await expect(todoPage.todoItems).toHaveCount(0);
    await expect(todoPage.footer).toBeHidden();
  });
});

test.describe("Task editing", () => {
  test("edit task text", async () => {
    await todoPage.addTodo("Buy milk");

    await todoPage.editTodo(0, "Buy oat milk");

    await expect(todoPage.todoItems).toHaveText(["Buy oat milk"]);
  });

  test("double click enters edit mode", async () => {
    await todoPage.addTodo("Buy milk");

    const field = await todoPage.startEditing(0);

    await expect(todoPage.item(0)).toHaveClass(/editing/);
    await expect(field).toHaveValue("Buy milk");
    await expect(field).toBeFocused();
  });

  test("cancel edit without changes keeps text", async () => {
    await todoPage.addTodos("Buy milk", "Walk the dog");
    await todoPage.startEditing(0);

    await todoPage.leaveEditByClickingOutside();

    await expect(todoPage.todoItems).toHaveText(["Buy milk", "Walk the dog"]);
    await expect(todoPage.item(0)).not.toHaveClass(/editing/);
  });

  test("save edited task on blur", async () => {
    await todoPage.addTodo("Buy milk");
    await todoPage.typeInEdit(0, "Buy bread");

    await todoPage.leaveEditByClickingOutside();

    await expect(todoPage.todoItems).toHaveText(["Buy bread"]);
  });

  test("editing to empty text deletes task", async () => {
    await todoPage.addTodos("Keep", "Remove by editing");

    await todoPage.editTodo(1, "");

    await expect(todoPage.todoItems).toHaveText(["Keep"]);
  });

  test("edited text is trimmed", async () => {
    await todoPage.addTodo("Buy milk");

    await todoPage.editTodo(0, "   Buy eggs   ");

    await expect(todoPage.todoItems).toHaveText(["Buy eggs"]);
  });
});
