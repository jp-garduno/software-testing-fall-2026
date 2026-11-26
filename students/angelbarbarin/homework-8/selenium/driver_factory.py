"""Creates the Chrome WebDriver used by the pytest suite and by the behave scenarios.

Defaults work on a normal machine (Selenium Manager finds Chrome and its driver). Optional
environment variables:

* HEADED=1                 show the browser window (default: headless)
* CHROME_BINARY=path       use a specific Chrome / Chromium executable
* CHROMEDRIVER_PATH=path   use a specific chromedriver instead of Selenium Manager
* CHROMEDRIVER_ARGS="..."  extra chromedriver flags, e.g. --disable-build-check
"""

import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def create_driver():
    """Start Chrome with a fixed window size so layouts (and screenshots) are comparable."""
    options = webdriver.ChromeOptions()
    if os.environ.get("HEADED") != "1":
        options.add_argument("--headless=new")
    for argument in ("--window-size=1280,900", "--no-sandbox", "--disable-dev-shm-usage"):
        options.add_argument(argument)
    if os.environ.get("CHROME_BINARY"):
        options.binary_location = os.environ["CHROME_BINARY"]

    service_args = os.environ.get("CHROMEDRIVER_ARGS", "").split()
    service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"), service_args=service_args)
    return webdriver.Chrome(options=options, service=service)
