const { test } = require("./fixtures");

test.beforeEach(async ({ todoPage }) => {
  for (const text of ["Task 1", "Task 2", "Task 3"]) {
    await todoPage.addTodo(text);
  }
  await todoPage.toggleTodo(1);
  await todoPage.expectCompleted(1);
});

test("view all tasks", async ({ todoPage }) => {
  await todoPage.filterActive();
  await todoPage.expectTodos(["Task 1", "Task 3"]);
  await todoPage.filterAll();
  await todoPage.expectTodos(["Task 1", "Task 2", "Task 3"]);
});

test("view active tasks only", async ({ todoPage }) => {
  await todoPage.filterActive();
  await todoPage.expectTodos(["Task 1", "Task 3"]);
  await todoPage.expectActiveCount(2);
});

test("view completed tasks only", async ({ todoPage }) => {
  await todoPage.filterCompleted();
  await todoPage.expectTodos(["Task 2"]);
  await todoPage.expectCompleted(0);
});
