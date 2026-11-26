const { Builder } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');

// Crea un Chrome para Selenium. Por defecto es headless para que funcione en CI (sin pantalla).
// Para ver el navegador en PowerShell: $env:HEADLESS='false'; npm test
async function buildDriver() {
  const options = new chrome.Options().addArguments('--window-size=1280,900');
  if (process.env.HEADLESS !== 'false')
    options.addArguments('--headless=new');

  return new Builder().forBrowser('chrome').setChromeOptions(options).build();
}

module.exports = { buildDriver };
