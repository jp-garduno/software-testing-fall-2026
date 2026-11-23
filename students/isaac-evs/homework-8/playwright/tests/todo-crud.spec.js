const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

let todoPage;

test.beforeEach(async ({ page }) => {
  todoPage = new TodoPage(page);
  await todoPage.openClean();
});

test.describe("Task creation", () => {
  test("create single task", async () => {
    await todoPage.addTodo("Buy milk");
    await expect(todoPage.todoItems).toHaveCount(1);
  });

  test("create multiple tasks keeps their order", async () => {
    await todoPage.addTodos("First", "Second", "Third");
    await expect(todoPage.todoItems).toHaveText(["First", "Second", "Third"]);
  });

  test("created task appears in the list as active", async () => {
    await todoPage.addTodo("Buy milk");
    await expect(todoPage.todoItems).toHaveText(["Buy milk"]);
    await expect(todoPage.item(0)).not.toHaveClass(/completed/);
    await expect(todoPage.itemsLeft).toContainText("1 item left");
  });

  test("input is emptied after adding", async () => {
    await todoPage.addTodo("Buy milk");
    await expect(todoPage.newTodoInput).toHaveValue("");
  });

  test("surrounding whitespace is trimmed", async () => {
    await todoPage.addTodo("   spaced out   ");
    await expect(todoPage.todoItems).toHaveText(["spaced out"]);
  });

  test("blank task is not created", async () => {
    await todoPage.addTodo("   ");
    await todoPage.addTodo("Real task"); // waits for a row, so the blank one has had its chance to appear
    await expect(todoPage.todoItems).toHaveText(["Real task"]);
  });

  test("markup is shown as text, not rendered", async () => {
    await todoPage.addTodo('<b>bold</b> & "quotes"');
    await expect(todoPage.todoItems).toHaveText(['<b>bold</b> & "quotes"']);
  });

  test("new list starts empty without footer", async () => {
    await expect(todoPage.todoItems).toHaveCount(0);
    await expect(todoPage.footer).toBeHidden();
  });
});

test.describe("Task completion", () => {
  test("mark task as complete", async () => {
    await todoPage.addTodo("Read book");
    await todoPage.toggleTodo(0);
    await expect(todoPage.item(0)).toHaveClass(/completed/);
  });

  test("unmark completed task", async () => {
    await todoPage.addTodo("Read book");
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(0);
    await expect(todoPage.item(0)).not.toHaveClass(/completed/);
  });

  test("complete multiple tasks", async () => {
    await todoPage.addTodos("One", "Two", "Three");
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);
    await expect(todoPage.item(0)).toHaveClass(/completed/);
    await expect(todoPage.item(1)).not.toHaveClass(/completed/);
    await expect(todoPage.item(2)).toHaveClass(/completed/);
  });

  test("items left counter follows completion", async () => {
    await todoPage.addTodos("One", "Two", "Three");
    await todoPage.toggleTodo(1);
    await expect(todoPage.itemsLeft).toContainText("2 items left");
  });

  test("toggle all completes every task", async () => {
    await todoPage.addTodos("One", "Two", "Three");
    await todoPage.toggleAllTodos();
    await expect(todoPage.todoItems).toHaveClass([
      /completed/,
      /completed/,
      /completed/,
    ]);
    await expect(todoPage.itemsLeft).toContainText("0 items left");
  });

  test("toggle all twice reopens every task", async () => {
    await todoPage.addTodos("One", "Two");
    await todoPage.toggleAllTodos();
    await todoPage.toggleAllTodos();
    await expect(todoPage.page.locator(".todo-list li.completed")).toHaveCount(
      0,
    );
  });
});

test.describe("Task deletion", () => {
  test("delete single task", async () => {
    await todoPage.addTodo("Task to delete");
    await todoPage.deleteTodo(0);
    await expect(todoPage.todoItems).toHaveCount(0);
  });

  test("delete only the chosen task", async () => {
    await todoPage.addTodos("Keep A", "Remove me", "Keep B");
    await todoPage.deleteTodo(1);
    await expect(todoPage.todoItems).toHaveText(["Keep A", "Keep B"]);
  });

  test("delete completed task", async () => {
    await todoPage.addTodos("Done task", "Open task");
    await todoPage.toggleTodo(0);
    await todoPage.deleteTodo(0);
    await expect(todoPage.todoItems).toHaveText(["Open task"]);
  });

  test("clear all completed", async () => {
    await todoPage.addTodos("Done 1", "Open", "Done 2");
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);
    await todoPage.clearCompleted();
    await expect(todoPage.todoItems).toHaveText(["Open"]);
  });

  test("clear completed is only offered when something is completed", async () => {
    await todoPage.addTodo("Open");
    await expect(todoPage.clearCompletedButton).toBeHidden();
    await todoPage.toggleTodo(0);
    await expect(todoPage.clearCompletedButton).toBeVisible();
  });

  test("footer disappears when the last task is deleted", async () => {
    await todoPage.addTodo("Only task");
    await expect(todoPage.footer).toBeVisible();
    await todoPage.deleteTodo(0);
    await expect(todoPage.footer).toBeHidden();
  });
});

test.describe("Task editing", () => {
  test("edit task text", async () => {
    await todoPage.addTodo("Buy milk");
    await todoPage.editTodo(0, "Buy oat milk");
    await expect(todoPage.todoItems).toHaveText(["Buy oat milk"]);
  });

  test("double click opens the task for editing", async () => {
    await todoPage.addTodo("Buy milk");
    await todoPage.startEdit(0);
    await expect(todoPage.item(0)).toHaveClass(/editing/);
    await expect(todoPage.item(0).locator(".edit")).toHaveValue("Buy milk");
  });

  test("save edited task by leaving the field", async () => {
    await todoPage.addTodos("Buy milk", "Walk dog");
    await todoPage.startEdit(1);
    await todoPage.typeInEdit(1, "Walk the dog");
    await todoPage.blurEdit();
    await expect(todoPage.todoItems).toHaveText(["Buy milk", "Walk the dog"]);
  });

  test("edited text is trimmed", async () => {
    await todoPage.addTodo("Buy milk");
    await todoPage.editTodo(0, "  Buy bread  ");
    await expect(todoPage.todoItems).toHaveText(["Buy bread"]);
  });

  test("editing a task to empty deletes it", async () => {
    await todoPage.addTodos("Keep", "Blank me");
    await todoPage.editTodo(1, "");
    await expect(todoPage.todoItems).toHaveText(["Keep"]);
  });

  test("editing keeps the completed state", async () => {
    await todoPage.addTodo("Buy milk");
    await todoPage.toggleTodo(0);
    await todoPage.editTodo(0, "Buy oat milk");
    await expect(todoPage.item(0)).toHaveClass(/completed/);
  });

  // Known defect of this TodoMVC build: the edit field only handles Enter, so Escape does not
  // cancel (the TodoMVC spec says it should). test.fail() makes this go red if the app is ever fixed.
  test("cancel edit with Escape restores the original text", async () => {
    test.fail(true, "TodoMVC React build ignores Escape in the edit field");
    await todoPage.addTodo("Buy milk");
    await todoPage.startEdit(0);
    await todoPage.typeInEdit(0, "Changed my mind");
    await todoPage.cancelEdit(0);
    await expect(todoPage.item(0)).not.toHaveClass(/editing/, {
      timeout: 2000,
    });
    await expect(todoPage.todoItems).toHaveText(["Buy milk"]);
  });
});
