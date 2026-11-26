import os

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome

APP_URL = os.environ.get("TODO_APP_URL", "https://todomvc.com/examples/react/dist/")


def create_driver():
    """Start Chrome, headless unless HEADED=1, at a fixed window size so layouts match between runs."""
    options = Options()
    if os.environ.get("HEADED") != "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-dev-shm-usage")
    return Chrome(options=options)
