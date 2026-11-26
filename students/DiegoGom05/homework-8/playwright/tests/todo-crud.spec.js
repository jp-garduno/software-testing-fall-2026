const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/todoPage");

test.describe("Todo CRUD", () => {
  let todoPage;

  // Cada test recibe una página nueva -> tests independientes
  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.navigate();
  });

  // ------------------------------------------------ 1. Creación
  test("create a single task", async () => {
    await todoPage.addTodo("Buy milk");

    await expect(todoPage.items).toHaveCount(1);
    await expect(todoPage.labels).toHaveText(["Buy milk"]);
  });

  test("create multiple tasks", async () => {
    const tasks = ["Task A", "Task B", "Task C"];
    for (const t of tasks) await todoPage.addTodo(t);

    await expect(todoPage.items).toHaveCount(3);
    await expect(todoPage.labels).toHaveText(tasks);
  });

  test("task appears in the list", async () => {
    await todoPage.addTodo("Visible task");

    expect(await todoPage.getVisibleTodos()).toContain("Visible task");
  });

  test("empty task is not created", async () => {
    await todoPage.addTodo("");

    await expect(todoPage.items).toHaveCount(0);
  });

  // ------------------------------------------------ 2. Completado
  test("complete a task", async () => {
    await todoPage.addTodo("Finish homework");

    await todoPage.toggleTodo(0);

    await expect(todoPage.item(0)).toHaveClass(/completed/);
  });

  test("uncomplete a task", async () => {
    await todoPage.addTodo("Toggle me");
    await todoPage.toggleTodo(0);
    await expect(todoPage.item(0)).toHaveClass(/completed/);

    await todoPage.toggleTodo(0);

    await expect(todoPage.item(0)).not.toHaveClass(/completed/);
  });

  test("complete multiple tasks", async () => {
    for (const t of ["One", "Two", "Three"]) await todoPage.addTodo(t);

    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);

    await expect(todoPage.item(0)).toHaveClass(/completed/);
    await expect(todoPage.item(1)).not.toHaveClass(/completed/);
    await expect(todoPage.item(2)).toHaveClass(/completed/);
  });

  // ------------------------------------------------ 3. Borrado
  test("delete a single task", async () => {
    await todoPage.addTodo("Task to delete");

    await todoPage.deleteTodo(0);

    await expect(todoPage.items).toHaveCount(0);
  });

  test("delete a completed task", async () => {
    await todoPage.addTodo("Done task");
    await todoPage.addTodo("Pending task");
    await todoPage.toggleTodo(0);

    await todoPage.deleteTodo(0);

    await expect(todoPage.labels).toHaveText(["Pending task"]);
  });

  test("clear all completed", async () => {
    for (const t of ["A", "B", "C"]) await todoPage.addTodo(t);
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(1);

    await todoPage.clearCompleted();

    await expect(todoPage.labels).toHaveText(["C"]);
  });

  // ------------------------------------------------ 4. Edición
  test("edit task text", async () => {
    await todoPage.addTodo("Old text");

    await todoPage.editTodo(0, "New text", true);

    await expect(todoPage.labels).toHaveText(["New text"]);
  });

  // En Selenium este escenario falló: Escape no salía del modo edición.
  // Si en Playwright también falla, deja test.fail() y documéntalo;
  // si pasa, quita test.fail() y anota la diferencia en el reporte.
  test("cancel edit", async () => {
    test.fail(
      false,
      "Cambia a true si Escape no cancela la edición en esta versión",
    );
    await todoPage.addTodo("Original");

    await todoPage.editTodo(0, "Changed", false); // Escape

    await expect(todoPage.labels).toHaveText(["Original"]);
  });

  test("save edited task persists after other actions", async () => {
    await todoPage.addTodo("Edit me");
    await todoPage.addTodo("Other");

    await todoPage.editTodo(0, "Edited", true);
    await todoPage.toggleTodo(1);

    await expect(todoPage.labels).toHaveText(["Edited", "Other"]);
  });

  test("edit to empty deletes the task", async () => {
    await todoPage.addTodo("Soon gone");

    await todoPage.editTodo(0, "", true);

    await expect(todoPage.items).toHaveCount(0);
  });
});
