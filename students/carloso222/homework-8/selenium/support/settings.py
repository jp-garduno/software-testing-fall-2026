"""Settings shared by the Selenium tests, the Behave steps and the performance script.

Every value can be overridden with an environment variable, so the same code runs
locally (headed or headless), in CI and against a local copy of the app.
"""

import os
from pathlib import Path

# The URL in the homework statement (https://todomvc.com/examples/react/) returns 404;
# the React example is served from /dist/.
DEFAULT_BASE_URL = "https://todomvc.com/examples/react/dist/"

BASE_URL = os.getenv("BASE_URL", DEFAULT_BASE_URL)
BROWSER = os.getenv("SELENIUM_BROWSER", "chrome").lower()
HEADLESS = os.getenv("HEADLESS", "1") != "0"
TIMEOUT = float(os.getenv("SELENIUM_TIMEOUT", "10"))
# WebDriverWait checks its condition every 0.5 s by default; 0.1 s makes every wait finish sooner.
POLL_FREQUENCY = float(os.getenv("SELENIUM_POLL", "0.1"))
SAVE_SCREENSHOTS = os.getenv("SAVE_SCREENSHOTS", "0") == "1"
# "eager" returns from driver.get() at DOMContentLoaded instead of waiting for third-party
# scripts (todomvc.com loads Google Analytics); the page object then waits for the app itself.
PAGE_LOAD_STRATEGY = os.getenv("SELENIUM_PAGE_LOAD", "eager")
WINDOW_SIZE = (1280, 720)

HOMEWORK_DIR = Path(__file__).resolve().parents[2]
SCREENSHOTS_DIR = HOMEWORK_DIR / "screenshots"
REPORTS_DIR = HOMEWORK_DIR / "reports"
