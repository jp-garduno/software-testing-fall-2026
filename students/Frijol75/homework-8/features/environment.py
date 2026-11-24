"""
Behave environment configuration for BDD scenarios.
Initializes and cleans up Selenium WebDriver per scenario.
"""

import os
import sys
from selenium import webdriver

# Ensure selenium/ is on sys.path so `from pages.todo_page import TodoPage` works
HOMEWORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELENIUM_DIR = os.path.join(HOMEWORK_DIR, "selenium")
if SELENIUM_DIR not in sys.path:
    sys.path.insert(0, SELENIUM_DIR)


def before_scenario(context, scenario):
    """Initialize a fresh browser before each BDD scenario."""
    options = webdriver.ChromeOptions()
    if os.environ.get("HEADLESS", "true").lower() != "false":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    context.driver = webdriver.Chrome(options=options)


def after_scenario(context, scenario):
    """Quit browser after each BDD scenario."""
    if hasattr(context, "driver") and context.driver:
        context.driver.quit()

