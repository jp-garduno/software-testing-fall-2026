from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_ARGS = (
    "--headless=new",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--window-size=1280,800",
)


def before_scenario(context, _scenario):
    options = Options()
    for arg in CHROME_ARGS:
        options.add_argument(arg)
    context.driver = webdriver.Chrome(options=options)  # pylint: disable=not-callable


def after_scenario(context, _scenario):
    if hasattr(context, "driver") and context.driver:
        context.driver.quit()
