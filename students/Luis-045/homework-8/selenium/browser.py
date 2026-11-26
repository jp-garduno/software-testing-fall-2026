"""Create an isolated Chrome session shared by pytest and Behave."""

import os

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver


def create_driver():
    """Start Chrome; Selenium Manager resolves the driver unless one is supplied."""
    options = Options()
    if os.getenv("HEADED") != "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--lang=en-US")
    if os.getenv("SELENIUM_BROWSER_BINARY"):
        options.binary_location = os.environ["SELENIUM_BROWSER_BINARY"]
    service = Service(executable_path=os.getenv("SELENIUM_DRIVER"))
    driver = WebDriver(service=service, options=options)
    driver.set_page_load_timeout(30)
    return driver
