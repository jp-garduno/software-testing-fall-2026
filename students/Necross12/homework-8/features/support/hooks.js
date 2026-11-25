const { Before, After, setDefaultTimeout, Status } = require('@cucumber/cucumber');
const { Builder } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');

// Para ver en el navegador, ejecuta en terminal $env:HEADLESS='false'; npm run test:bdd
// Las operaciones del navegador tardan más que el timeout por defecto de Cucumber (5 s)
setDefaultTimeout(30000);

// Cada escenario usa un navegador nuevo para que las pruebas sean independientes
Before(async function () {
  const options = new chrome.Options();
  if (process.env.HEADLESS !== 'false')
    options.addArguments('--headless=new');

  this.driver = await new Builder().forBrowser('chrome').setChromeOptions(options).build();
});

After(async function (scenario) {
  if (this.driver) {
    // Evidencia visual cuando un escenario falla
    if (scenario.result.status === Status.FAILED && this.todoPage)
      await this.todoPage.takeScreenshot(`bdd-failed-${scenario.pickle.name}`);
    await this.driver.quit();
  }
});
