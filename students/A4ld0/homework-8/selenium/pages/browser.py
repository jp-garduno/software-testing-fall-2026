"""Shared WebDriver configuration for pytest and Behave."""

import os

from selenium import webdriver


def create_driver():
    options = webdriver.ChromeOptions()
    if os.getenv("HEADED") != "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver

