const { Given, When, Then } = require('@cucumber/cucumber');
const assert = require('assert');
const { TodoPage } = require('../../selenium/pages/TodoPage');

Given('I am on the todo page', async function () {
  this.todoPage = new TodoPage(this.driver);
  await this.todoPage.navigate();
});

When('I add a todo {string}', async function (text) {
  await this.todoPage.addTodo(text);
});

Given('I have a todo {string}', async function (text) {
  await this.todoPage.addTodo(text);
});

// 1 para cubre y 0 para no cubre 
Then(/^I should see (\d+) todos?(?:\(s\))?$/, async function (count) {
  const expected = Number(count);
  const actualCount = await this.todoPage.getTodoCount();
  assert.strictEqual(
    actualCount,
    expected,
    `Expected ${expected}, got ${actualCount}`
  );
});

Then('the todo should be {string}', async function (text) {
  const todos = await this.todoPage.getVisibleTodos();
  assert.ok(
    todos.includes(text),
    `Expected to find "${text}" among ${JSON.stringify(todos)}`
  );
});

When('I mark the todo as complete', async function () {
  await this.todoPage.toggleTodo(0);
});

Then('the todo should be marked as done', async function () {
  const done = await this.todoPage.isTodoCompleted(0);
  assert.strictEqual(done, true, 'Expected the todo to be marked as completed');
});

Then('the active count should be {int}', async function (count) {
  const activeCount = await this.todoPage.getActiveCount();
  assert.strictEqual(
    activeCount,
    count,
    `Expected active count ${count}, got ${activeCount}`
  );
});

When('I delete the todo', async function () {
  await this.todoPage.deleteTodo(0);
});

// Tabla de datos del Scenario Outline
Given('I have the following todos:', async function (dataTable) {
  const rows = dataTable.hashes(); // [{ text, completed }, ...]

  for (const row of rows)
    await this.todoPage.addTodo(row.text);

  for (let index = 0; index < rows.length; index++)
    if (rows[index].completed === 'true')
      await this.todoPage.toggleTodo(index);
});

When('I filter by {string}', async function (filterName) {
  const normalized = filterName.trim().toLowerCase();
  if (normalized === 'all')
    await this.todoPage.filterAll();
  else if 
  (normalized === 'active')
    await this.todoPage.filterActive();
  else if 
  (normalized === 'completed')
    await this.todoPage.filterCompleted();
  else
    throw new Error(`Unknown filter: ${filterName}`);
});
