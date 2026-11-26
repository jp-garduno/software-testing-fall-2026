"""Behave hooks. The steps reuse the Selenium page object, so selenium/ goes on the import path first.

One Firefox serves every scenario. The Background step loads the app again for each of them, and
since TodoMVC keeps its todos in memory, every scenario starts with an empty list.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "selenium"))

from firefox_driver import start_firefox  # pylint: disable=wrong-import-position


def before_all(context):
    context.driver = start_firefox()


def after_all(context):
    context.driver.quit()
