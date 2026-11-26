const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/todoPage");

test.describe("Todo filters", () => {
  let todoPage;

  // Escenario base: Active 1, Completed 1 (completada), Active 2
  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.navigate();
    for (const t of ["Active 1", "Completed 1", "Active 2"]) {
      await todoPage.addTodo(t);
    }
    await todoPage.toggleTodo(1);
    await expect(todoPage.item(1)).toHaveClass(/completed/);
  });

  test("filter all", async () => {
    await todoPage.filterActive(); // nos movemos a otra vista primero
    await expect(todoPage.items).toHaveCount(2);

    await todoPage.filterAll();

    await expect(todoPage.labels).toHaveText([
      "Active 1",
      "Completed 1",
      "Active 2",
    ]);
  });

  test("filter active", async () => {
    await todoPage.filterActive();

    await expect(todoPage.labels).toHaveText(["Active 1", "Active 2"]);
  });

  test("filter completed", async () => {
    await todoPage.filterCompleted();

    await expect(todoPage.labels).toHaveText(["Completed 1"]);
  });

  test("filter is reflected in the URL", async ({ page }) => {
    await todoPage.filterActive();

    await expect(page).toHaveURL(/#\/active$/);
    await expect(todoPage.items).toHaveCount(2);
  });

  test("completing a task in Active view removes it", async () => {
    await todoPage.filterActive();
    await expect(todoPage.items).toHaveCount(2);

    await todoPage.toggleTodo(0);

    await expect(todoPage.labels).toHaveText(["Active 2"]);
  });
});
