"""Shared WebDriver configuration for pytest and Behave."""

import os

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


def create_driver():
    options = Options()
    chrome_binary = os.getenv("CHROME_BIN")
    if chrome_binary:
        options.binary_location = chrome_binary
    if os.getenv("HEADED") != "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-dev-shm-usage")
    driver = WebDriver(options=options)
    driver.set_page_load_timeout(30)
    return driver
