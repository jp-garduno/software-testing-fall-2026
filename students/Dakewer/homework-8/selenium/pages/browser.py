"""WebDriver factory shared by the pytest fixtures and the Behave hooks."""
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def create_driver():
    """Start Chrome.

    Environment variables (all optional):
      HEADLESS=0      show the browser window
      CHROME_BINARY   use a specific Chrome/Chromium executable
      CHROMEDRIVER    use a specific chromedriver (otherwise Selenium Manager picks one)
    """
    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "1") != "0":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    # Stop Chrome's own update/sign-in traffic from adding noise to the runs.
    options.add_argument("--disable-background-networking")
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        # Chrome refuses to start its sandbox as root (common in containers).
        options.add_argument("--no-sandbox")
    if os.getenv("CHROME_BINARY"):
        options.binary_location = os.environ["CHROME_BINARY"]

    service = Service(executable_path=os.getenv("CHROMEDRIVER") or None)
    return webdriver.Chrome(options=options, service=service)
