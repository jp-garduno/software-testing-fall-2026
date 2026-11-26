// Bonus A: visual regression with Playwright's built-in screenshot comparison.
const { test, expect } = require('@playwright/test');
const { TodoPage } = require('../../pages/TodoPage');

let todoPage;

test.beforeEach(async ({ page }) => {
  todoPage = new TodoPage(page);
  await todoPage.navigate();
});

async function compare(page, name) {
  // Set VISUAL_DEMO_CHANGE=1 to inject a style change and see a diff report.
  if (process.env.VISUAL_DEMO_CHANGE) {
    await page.addStyleTag({ content: '.header h1 { color: #2563eb !important; }' });
  }
  // Move the pointer away so hover styles never leak into a screenshot.
  await page.mouse.move(0, 0);
  await expect(page).toHaveScreenshot(`${name}.png`, { fullPage: true });
}

async function seed() {
  await todoPage.addTodos('Buy groceries', 'Read book', 'Walk the dog');
  await todoPage.toggleTodo(1);
}

test('empty state', async ({ page }) => {
  await compare(page, 'empty-state');
});

test('list with a completed task', async ({ page }) => {
  await seed();
  await compare(page, 'mixed-list');
});

test('active filter', async ({ page }) => {
  await seed();
  await todoPage.filterActive();
  await compare(page, 'filter-active');
});

test('completed filter', async ({ page }) => {
  await seed();
  await todoPage.filterCompleted();
  await compare(page, 'filter-completed');
});

test('edit mode', async ({ page }) => {
  await seed();
  await todoPage.startEdit(0);
  await compare(page, 'edit-mode');
});
