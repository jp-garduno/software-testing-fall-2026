"""Creates WebDriver instances for Chrome, Firefox or Edge.

Selenium Manager (bundled with Selenium 4.6+) downloads the matching driver
automatically, so no chromedriver/geckodriver has to be installed by hand.
"""

import sys

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from support import settings  # pylint: disable=wrong-import-order


def _chrome(headless: bool, page_load_strategy: str) -> WebDriver:
    options = webdriver.ChromeOptions()
    options.page_load_strategy = page_load_strategy
    if headless:
        options.add_argument("--headless=new")
    if sys.platform.startswith("linux"):
        # Needed inside containers and GitHub Actions runners.
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def _firefox(headless: bool, page_load_strategy: str) -> WebDriver:
    options = webdriver.FirefoxOptions()
    options.page_load_strategy = page_load_strategy
    if headless:
        options.add_argument("-headless")
    return webdriver.Firefox(options=options)


def _edge(headless: bool, page_load_strategy: str) -> WebDriver:
    options = webdriver.EdgeOptions()
    options.page_load_strategy = page_load_strategy
    if headless:
        options.add_argument("--headless=new")
    return webdriver.Edge(options=options)


_FACTORIES = {"chrome": _chrome, "firefox": _firefox, "edge": _edge}


def create_driver(
    browser: str = settings.BROWSER,
    headless: bool = settings.HEADLESS,
    page_load_strategy: str = settings.PAGE_LOAD_STRATEGY,
) -> WebDriver:
    """Start a browser session with the window size shared by every suite."""
    try:
        factory = _FACTORIES[browser]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported browser '{browser}'. Use one of: {', '.join(_FACTORIES)}"
        ) from exc
    driver = factory(headless, page_load_strategy)
    driver.set_window_size(*settings.WINDOW_SIZE)
    return driver
