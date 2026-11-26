// Bonus C: métricas de rendimiento.
// Mide, con Selenium y con Playwright (ambos en Chrome headless):
//   - tiempo de arranque del navegador
//   - tiempo de carga de la página (Navigation Timing API)
//   - tiempo de cada operación del Page Object (agregar, completar, filtrar, editar, eliminar)
// Uso: npm run perf   (opcional: RUNS=10 npm run perf)
const fs = require('fs');
const path = require('path');
const { Builder } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const { chromium } = require('playwright');
const { TodoPage: SeleniumTodoPage } = require('../selenium/pages/TodoPage');
const { TodoPage: PlaywrightTodoPage } = require('../playwright/pages/TodoPage');

const RUNS = Number(process.env.RUNS || 5);

async function time(fn) {
  const start = performance.now();
  await fn();
  return performance.now() - start;
}

// Ejecuta el mismo flujo con cualquiera de los dos Page Objects
async function measureOperations(todoPage, getNavTiming) {
  const r = {};
  r.navigate = await time(() => todoPage.navigate());
  Object.assign(r, await getNavTiming());
  r.addTodo = await time(() => todoPage.addTodo('Tarea de rendimiento'));
  r.add3Todos = await time(() => todoPage.addTodos(['A', 'B', 'C']));
  r.toggleTodo = await time(() => todoPage.toggleTodo(1));
  r.filterActive = await time(() => todoPage.filterActive());
  r.filterCompleted = await time(() => todoPage.filterCompleted());
  r.filterAll = await time(() => todoPage.filterAll());
  r.getVisibleTodos = await time(() => todoPage.getVisibleTodos());
  r.editTodo = await time(() => todoPage.editTodo(0, 'Editada'));
  r.deleteTodo = await time(() => todoPage.deleteTodo(0));
  r.clearCompleted = await time(() => todoPage.clearCompleted());
  return r;
}

const NAV_TIMING_JS = `
  const n = performance.getEntriesByType('navigation')[0];
  return { ttfb: n.responseStart - n.startTime,
           domContentLoaded: n.domContentLoadedEventEnd - n.startTime,
           loadEvent: n.loadEventEnd - n.startTime };`;

async function runSelenium() {
  const runs = [];
  for (let i = 0; i < RUNS; i++) {
    let driver;
    const launch = await time(async () => {
      const options = new chrome.Options().addArguments('--headless=new');
      driver = await new Builder().forBrowser('chrome').setChromeOptions(options).build();
    });
    const ops = await measureOperations(new SeleniumTodoPage(driver), () =>
      driver.executeScript(NAV_TIMING_JS)
    );
    await driver.quit();
    runs.push({ launch, ...ops });
  }
  return runs;
}

async function runPlaywright() {
  const runs = [];
  for (let i = 0; i < RUNS; i++) {
    let browser;
    let page;
    const launch = await time(async () => {
      browser = await chromium.launch({ headless: true });
      page = await browser.newPage();
    });
    const ops = await measureOperations(new PlaywrightTodoPage(page), () =>
      page.evaluate(new Function(NAV_TIMING_JS))
    );
    await browser.close();
    runs.push({ launch, ...ops });
  }
  return runs;
}

function summarize(runs) {
  const summary = {};
  for (const key of Object.keys(runs[0])) {
    const values = runs.map((r) => r[key]).sort((a, b) => a - b);
    const avg = values.reduce((a, b) => a + b, 0) / values.length;
    summary[key] = {
      avg: Math.round(avg),
      median: Math.round(values[Math.floor(values.length / 2)]),
      min: Math.round(values[0]),
      max: Math.round(values[values.length - 1]),
    };
  }
  return summary;
}

(async () => {
  console.log(`Midiendo ${RUNS} ejecuciones por herramienta...`);
  const selenium = summarize(await runSelenium());
  const playwright = summarize(await runPlaywright());

  const rows = Object.keys(selenium).map((key) => ({
    metrica: key,
    'Selenium prom (ms)': selenium[key].avg,
    'Playwright prom (ms)': playwright[key].avg,
    'Selenium mediana': selenium[key].median,
    'Playwright mediana': playwright[key].median,
  }));
  console.table(rows);

  const outFile = path.join(__dirname, 'results.json');
  fs.writeFileSync(
    outFile,
    JSON.stringify({ date: new Date().toISOString(), runs: RUNS, selenium, playwright }, null, 2)
  );
  console.log(`Resultados guardados en ${outFile}`);
})();
