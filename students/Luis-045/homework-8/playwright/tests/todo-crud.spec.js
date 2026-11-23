const { test } = require("./fixtures");

test("create single task", async ({ todoPage }) => {
  await todoPage.addTodo("Buy milk");
  await todoPage.expectTodos(["Buy milk"]);
  await todoPage.expectActiveCount(1);
});

test("create multiple tasks", async ({ todoPage }) => {
  const tasks = ["Buy milk", "Read book", "Study testing"];
  for (const task of tasks) {
    await todoPage.addTodo(task);
  }
  await todoPage.expectTodos(tasks);
  await todoPage.expectActiveCount(3);
});

test("task appears in list", async ({ todoPage }) => {
  const text = "Revisar tarea 8: café & pruebas";
  await todoPage.addTodo(text);
  await todoPage.expectTodos([text]);
  await todoPage.expectCompleted(0, false);
});

test("mark task complete", async ({ todoPage }) => {
  await todoPage.addTodo("Read book");
  await todoPage.toggleTodo(0);
  await todoPage.expectCompleted(0);
  await todoPage.expectActiveCount(0);
});

test("unmark completed task", async ({ todoPage }) => {
  await todoPage.addTodo("Read book");
  await todoPage.toggleTodo(0);
  await todoPage.expectCompleted(0);
  await todoPage.toggleTodo(0);
  await todoPage.expectCompleted(0, false);
  await todoPage.expectActiveCount(1);
});

test("complete multiple tasks", async ({ todoPage }) => {
  await todoPage.addTodo("First");
  await todoPage.addTodo("Second");
  await todoPage.toggleTodo(0);
  await todoPage.toggleTodo(1);
  await todoPage.expectCompleted(0);
  await todoPage.expectCompleted(1);
  await todoPage.expectActiveCount(0);
});

test("delete single task", async ({ todoPage }) => {
  await todoPage.addTodo("Keep");
  await todoPage.addTodo("Remove");
  await todoPage.deleteTodo(1);
  await todoPage.expectTodos(["Keep"]);
  await todoPage.expectActiveCount(1);
});

test("delete completed task", async ({ todoPage }) => {
  await todoPage.addTodo("Keep");
  await todoPage.addTodo("Done");
  await todoPage.toggleTodo(1);
  await todoPage.expectCompleted(1);
  await todoPage.deleteTodo(1);
  await todoPage.expectTodos(["Keep"]);
  await todoPage.expectActiveCount(1);
});

test("clear all completed", async ({ todoPage }) => {
  for (const task of ["Done one", "Keep", "Done two"]) {
    await todoPage.addTodo(task);
  }
  await todoPage.toggleTodo(0);
  await todoPage.toggleTodo(2);
  await todoPage.clearCompleted();
  await todoPage.expectTodos(["Keep"]);
  await todoPage.expectActiveCount(1);
});

test("edit task text and save on blur", async ({ todoPage }) => {
  await todoPage.addTodo("Old title");
  await todoPage.beginEdit(0);
  await todoPage.replaceEditText("Updated title");
  await todoPage.expectEditText("Updated title");
  await todoPage.blurEdit();
  await todoPage.expectTodos(["Updated title"]);
});

test("cancel edit", async ({ todoPage }) => {
  await todoPage.addTodo("Original title");
  await todoPage.beginEdit(0);
  await todoPage.replaceEditText("Discard this draft");
  test.fail(
    process.env.VERIFY_KNOWN_DEFECTS !== "1",
    "TODO-001: deployed TodoMVC ignores Escape in the inline editor",
  );
  await todoPage.cancelEdit();
  await todoPage.expectTodos(["Original title"]);
});

test("save edited task", async ({ todoPage }) => {
  await todoPage.addTodo("Old title");
  await todoPage.beginEdit(0);
  await todoPage.replaceEditText("Saved title");
  await todoPage.finishEdit();
  await todoPage.expectTodos(["Saved title"]);
});

test("ignore whitespace only task", async ({ todoPage }) => {
  await todoPage.addTodo("   ");
  await todoPage.expectTodos([]);
});

test("trim new task text", async ({ todoPage }) => {
  await todoPage.addTodo("  Trim this title  ");
  await todoPage.expectTodos(["Trim this title"]);
});

test("empty edit deletes task", async ({ todoPage }) => {
  await todoPage.addTodo("Remove by editing");
  await todoPage.beginEdit(0);
  await todoPage.replaceEditText("");
  await todoPage.finishEdit();
  await todoPage.expectTodos([]);
});
