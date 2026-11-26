const { test, expect } = require("../fixtures");

test.beforeEach(async ({ todoPage }) => {
  await todoPage.addTodo("Task 1", "Task 2", "Task 3");
  await todoPage.toggleTodo(1);
});

const FILTER_CASES = [
  { filter: "All", expected: ["Task 1", "Task 2", "Task 3"] },
  { filter: "Active", expected: ["Task 1", "Task 3"] },
  { filter: "Completed", expected: ["Task 2"] },
];

for (const { filter, expected } of FILTER_CASES) {
  test(`filter by ${filter}: shows matching tasks`, async ({ todoPage }) => {
    await todoPage.filterBy(filter);

    await expect(todoPage.labels).toHaveText(expected);
  });

  test(`filter by ${filter}: highlights chosen filter`, async ({ todoPage }) => {
    await todoPage.filterBy(filter);

    await expect(todoPage.selectedFilter).toHaveText(filter);
  });
}

test("filter active: completing task hides it", async ({ todoPage }) => {
  await todoPage.filterActive();

  await todoPage.toggleTodo(0);

  await expect(todoPage.labels).toHaveText(["Task 3"]);
});

test("filter completed: new task is not listed", async ({ todoPage }) => {
  await todoPage.filterCompleted();

  await todoPage.addTodo("Task 4");

  await expect(todoPage.labels).toHaveText(["Task 2"]);
  await expect(todoPage.counter).toHaveText("3 items left!");
});

test("filter all after other filter: lists every task again", async ({ todoPage }) => {
  await todoPage.filterCompleted();

  await todoPage.filterBy("All");

  await expect(todoPage.items).toHaveCount(3);
});

test("filter active: counter ignores filter", async ({ todoPage }) => {
  await todoPage.filterCompleted();

  await expect(todoPage.counter).toHaveText("2 items left!");
});
