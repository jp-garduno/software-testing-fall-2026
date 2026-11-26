"""Create an isolated Chrome session with Selenium Manager."""

import os

from selenium import webdriver


def create_driver():
    """Return a fresh headless browser; never reuse a user's profile."""
    options = webdriver.ChromeOptions()
    if os.getenv("HEADED") != "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    if os.getenv("CHROME_BINARY"):
        options.binary_location = os.environ["CHROME_BINARY"]
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver
