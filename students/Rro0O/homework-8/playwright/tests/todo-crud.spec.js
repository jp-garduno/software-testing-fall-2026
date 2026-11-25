/** Task creation, completion, deletion and editing. */

const { test, expect } = require("./fixtures");

test.describe("Task creation", () => {
  test("create single task", async ({ todoPage }) => {
    await todoPage.addTodo("Buy milk");

    await expect(todoPage.itemLabels).toHaveText(["Buy milk"]);
    await expect(todoPage.counter).toHaveText("1 item left!");
  });

  test("create multiple tasks", async ({ todoPage }) => {
    await todoPage.addTodos("Buy milk", "Walk the dog", "Read book");

    await expect(todoPage.todoItems).toHaveCount(3);
    await expect(todoPage.counter).toHaveText("3 items left!");
  });

  test("new task appears at end of list and input is trimmed", async ({ todoPage }) => {
    await todoPage.addTodos("First", "   Second with spaces   ");

    await expect(todoPage.itemLabels).toHaveText(["First", "Second with spaces"]);
  });

  test("blank task is not created", async ({ todoPage }) => {
    await todoPage.addTodo("     ");

    await expect(todoPage.todoItems).toHaveCount(0);
    await expect(todoPage.counter).toBeHidden();
  });
});

test.describe("Task completion", () => {
  test("mark task as complete", async ({ todoPage }) => {
    await todoPage.addTodo("Read book");

    await todoPage.toggleTodo(0);

    await expect(todoPage.item(0)).toHaveClass(/completed/);
    await expect(todoPage.counter).toHaveText("0 items left!");
  });

  test("unmark completed task", async ({ todoPage }) => {
    await todoPage.addTodo("Read book");
    await todoPage.toggleTodo(0);

    await todoPage.toggleTodo(0);

    await expect(todoPage.item(0)).not.toHaveClass(/completed/);
    await expect(todoPage.counter).toHaveText("1 item left!");
  });

  test("complete multiple tasks", async ({ todoPage }) => {
    await todoPage.addTodos("One", "Two", "Three");

    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);

    await expect(todoPage.item(0)).toHaveClass(/completed/);
    await expect(todoPage.item(1)).not.toHaveClass(/completed/);
    await expect(todoPage.item(2)).toHaveClass(/completed/);
    await expect(todoPage.counter).toHaveText("1 item left!");
  });

  test("toggle all completes every task", async ({ todoPage }) => {
    await todoPage.addTodos("One", "Two", "Three");

    await todoPage.toggleAll();

    await expect(todoPage.completedItems).toHaveCount(3);
    await expect(todoPage.counter).toHaveText("0 items left!");
  });
});

test.describe("Task deletion", () => {
  test("delete single task", async ({ todoPage }) => {
    await todoPage.addTodos("Keep me", "Delete me");

    await todoPage.deleteTodo(1);

    await expect(todoPage.itemLabels).toHaveText(["Keep me"]);
  });

  test("delete completed task", async ({ todoPage }) => {
    await todoPage.addTodo("Done task");
    await todoPage.toggleTodo(0);

    await todoPage.deleteTodo(0);

    await expect(todoPage.todoItems).toHaveCount(0);
    await expect(todoPage.counter).toBeHidden();
  });

  test("clear all completed tasks", async ({ todoPage }) => {
    await todoPage.addTodos("One", "Two", "Three");
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);

    await todoPage.clearCompleted();

    await expect(todoPage.itemLabels).toHaveText(["Two"]);
    await expect(todoPage.clearCompletedButton).toBeHidden();
  });
});

test.describe("Task editing", () => {
  test("edit task text", async ({ todoPage }) => {
    await todoPage.addTodo("Original text");

    await todoPage.editTodo(0, "Updated text");

    await expect(todoPage.itemLabels).toHaveText(["Updated text"]);
  });

  test("cancel edit without changes keeps original", async ({ todoPage }) => {
    await todoPage.addTodo("Original text");
    await todoPage.startEdit(0);

    await todoPage.blurEdit();

    await expect(todoPage.editInputs).toHaveCount(0);
    await expect(todoPage.itemLabels).toHaveText(["Original text"]);
  });

  test("escape cancels edit", async ({ todoPage }) => {
    // Playwright reports this as passed only while it fails, so a fix in the app turns it red.
    test.fail(true, "Application defect: the edit field ignores Escape, although the TodoMVC spec discards the edit");
    await todoPage.addTodo("Original text");
    await todoPage.startEdit(0);
    await todoPage.typeInEdit(0, "Discard me");

    await todoPage.pressEscapeInEdit(0);

    await expect(todoPage.editInputs, "Escape should leave edit mode").toHaveCount(0, { timeout: 1000 });
    await expect(todoPage.itemLabels).toHaveText(["Original text"]);
  });

  test("save edited task on blur", async ({ todoPage }) => {
    await todoPage.addTodo("Original text");
    await todoPage.startEdit(0);
    await todoPage.typeInEdit(0, "Saved by blur");

    await todoPage.blurEdit();

    await expect(todoPage.itemLabels).toHaveText(["Saved by blur"]);
  });

  test("saving empty text deletes task", async ({ todoPage }) => {
    await todoPage.addTodo("Soon gone");

    await todoPage.editTodo(0, "");

    await expect(todoPage.todoItems).toHaveCount(0);
  });
});
