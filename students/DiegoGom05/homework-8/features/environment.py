import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SELENIUM_DIR = os.path.abspath(os.path.join(HERE, "..", "selenium"))
if SELENIUM_DIR not in sys.path:
    sys.path.insert(0, SELENIUM_DIR)

from selenium import webdriver  # noqa: E402


def before_scenario(context, scenario):
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    context.driver = webdriver.Chrome(options=opts)


def after_scenario(context, scenario):
    context.driver.quit()
