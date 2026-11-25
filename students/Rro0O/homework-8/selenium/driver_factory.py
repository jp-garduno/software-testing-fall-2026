"""Single place where the WebDriver is configured.

Set HEADED=1 to see the browser window.
"""

import os

from selenium import webdriver


def create_driver():
    """Return a new, isolated Chrome WebDriver. Selenium Manager resolves the driver binary."""
    options = webdriver.ChromeOptions()
    if os.environ.get("HEADED") != "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    # Both flags are needed on CI containers.
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)
