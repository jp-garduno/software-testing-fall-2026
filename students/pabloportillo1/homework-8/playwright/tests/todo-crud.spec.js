const { test, expect } = require("../fixtures");

test.describe("task creation", () => {
  test("add todo: single task appears in list", async ({ todoPage }) => {
    await todoPage.addTodo("Buy milk");

    await expect(todoPage.labels).toHaveText(["Buy milk"]);
  });

  test("add todo: several tasks keep entry order", async ({ todoPage }) => {
    await todoPage.addTodo("Buy milk", "Walk the dog", "Pay rent");

    await expect(todoPage.labels).toHaveText(["Buy milk", "Walk the dog", "Pay rent"]);
  });

  test("add todo: several tasks counted as items left", async ({ todoPage }) => {
    await todoPage.addTodo("Buy milk", "Walk the dog");

    await expect(todoPage.counter).toHaveText("2 items left!");
  });

  test("add todo: surrounding spaces are trimmed", async ({ todoPage }) => {
    await todoPage.addTodo("   Call mom   ");

    await expect(todoPage.labels).toHaveText(["Call mom"]);
  });

  test("add todo: blank text is ignored", async ({ todoPage }) => {
    await todoPage.addTodo("     ");

    await expect(todoPage.items).toHaveCount(0);
  });

  test("add todo: markup is shown as plain text", async ({ todoPage }) => {
    await todoPage.addTodo("<b>Bold</b> plan");

    await expect(todoPage.labels).toHaveText(["<b>Bold</b> plan"]);
  });
});

test.describe("task completion", () => {
  test("toggle todo: marks task completed", async ({ todoPage }) => {
    await todoPage.addTodo("Read book");

    await todoPage.toggleTodo(0);

    await expect(todoPage.item(0)).toHaveClass(/completed/);
    await expect(todoPage.counter).toHaveText("0 items left!");
  });

  test("toggle todo twice: unmarks task", async ({ todoPage }) => {
    await todoPage.addTodo("Read book");
    await todoPage.toggleTodo(0);

    await todoPage.toggleTodo(0);

    await expect(todoPage.item(0)).not.toHaveClass(/completed/);
    await expect(todoPage.counter).toHaveText("1 item left!");
  });

  test("toggle todo: several tasks leave others active", async ({ todoPage }) => {
    await todoPage.addTodo("Task 1", "Task 2", "Task 3");

    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);

    await expect(todoPage.items).toHaveClass([/completed/, /^$/, /completed/]);
  });

  test("toggle todo: single remaining task uses singular counter", async ({ todoPage }) => {
    await todoPage.addTodo("Task 1", "Task 2");

    await todoPage.toggleTodo(0);

    await expect(todoPage.counter).toHaveText("1 item left!");
  });

  test("toggle all: marks every task completed", async ({ todoPage }) => {
    await todoPage.addTodo("Task 1", "Task 2", "Task 3");

    await todoPage.toggleAll();

    await expect(todoPage.counter).toHaveText("0 items left!");
  });

  test("toggle all twice: reactivates every task", async ({ todoPage }) => {
    await todoPage.addTodo("Task 1", "Task 2");
    await todoPage.toggleAll();

    await todoPage.toggleAll();

    await expect(todoPage.items).toHaveClass([/^$/, /^$/]);
  });
});

test.describe("task deletion", () => {
  test("delete todo: removes only that task", async ({ todoPage }) => {
    await todoPage.addTodo("Keep me", "Delete me", "Keep me too");

    await todoPage.deleteTodo(1);

    await expect(todoPage.labels).toHaveText(["Keep me", "Keep me too"]);
  });

  test("delete todo: completed task is removed", async ({ todoPage }) => {
    await todoPage.addTodo("Done task", "Open task");
    await todoPage.toggleTodo(0);

    await todoPage.deleteTodo(0);

    await expect(todoPage.labels).toHaveText(["Open task"]);
    await expect(todoPage.counter).toHaveText("1 item left!");
  });

  test("clear completed: removes every completed task", async ({ todoPage }) => {
    await todoPage.addTodo("Task 1", "Task 2", "Task 3");
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);

    await todoPage.clearCompleted();

    await expect(todoPage.labels).toHaveText(["Task 2"]);
  });

  test("clear completed: hidden without completed tasks", async ({ todoPage }) => {
    await todoPage.addTodo("Task 1");

    await expect(todoPage.clearCompletedButton).toBeHidden();
  });
});

test.describe("task editing", () => {
  test("open editor: shows current text", async ({ todoPage }) => {
    await todoPage.addTodo("Original text");

    const editor = await todoPage.openEditor(0);

    await expect(editor).toHaveValue("Original text");
    await expect(todoPage.item(0)).toHaveClass(/editing/);
  });

  test("edit todo: new text is saved", async ({ todoPage }) => {
    await todoPage.addTodo("Buy milk", "Walk the dog");

    await todoPage.editTodo(0, "Buy oat milk");

    await expect(todoPage.labels).toHaveText(["Buy oat milk", "Walk the dog"]);
  });

  test("edit todo: surrounding spaces are trimmed", async ({ todoPage }) => {
    await todoPage.addTodo("Buy milk");

    await todoPage.editTodo(0, "  Buy bread  ");

    await expect(todoPage.labels).toHaveText(["Buy bread"]);
  });

  test("edit todo: empty text deletes task", async ({ todoPage }) => {
    await todoPage.addTodo("Buy milk", "Walk the dog");

    await todoPage.editTodo(0, "");

    await expect(todoPage.labels).toHaveText(["Walk the dog"]);
  });

  test("edit todo: keeps completed state", async ({ todoPage }) => {
    await todoPage.addTodo("Buy milk");
    await todoPage.toggleTodo(0);

    await todoPage.editTodo(0, "Buy oat milk");

    await expect(todoPage.labels).toHaveText(["Buy oat milk"]);
    await expect(todoPage.item(0)).toHaveClass(/completed/);
  });

  test(
    "cancel editing: escape discards changes",
    {
      annotation: {
        type: "known defect",
        description:
          "The TodoMVC spec says Escape discards the edit, but this React build ignores Escape " +
          "and keeps the editor open with the changed text",
      },
    },
    async ({ todoPage }) => {
      test.fail();
      await todoPage.addTodo("Buy milk");
      await todoPage.startEditing(0, "Something else");

      await todoPage.cancelEditing();

      await expect(todoPage.item(0)).not.toHaveClass(/editing/, { timeout: 1000 });
      await expect(todoPage.labels).toHaveText(["Buy milk"]);
    },
  );
});
