const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

test.describe("Bonus: Performance Metrics", () => {
  test("measure page load and CRUD operation times", async ({ page }) => {
    const todoPage = new TodoPage(page);

    const loadStart = Date.now();
    await todoPage.navigate();
    const loadTimeMs = Date.now() - loadStart;

    const addStart = Date.now();
    for (let i = 1; i <= 5; i++) {
      await todoPage.addTodo(`Perf Task ${i}`);
    }
    const addFiveTimeMs = Date.now() - addStart;

    const filterStart = Date.now();
    await todoPage.toggleTodo(0);
    await todoPage.filterActive();
    await todoPage.filterCompleted();
    await todoPage.filterAll();
    const filterTimeMs = Date.now() - filterStart;

    console.log(
      `[Perf] Load: ${loadTimeMs}ms | Add 5 tasks: ${addFiveTimeMs}ms | Filter cycle: ${filterTimeMs}ms`
    );

    expect(loadTimeMs).toBeLessThan(10000);
    expect(addFiveTimeMs).toBeLessThan(5000);
    expect(filterTimeMs).toBeLessThan(3000);
  });
});