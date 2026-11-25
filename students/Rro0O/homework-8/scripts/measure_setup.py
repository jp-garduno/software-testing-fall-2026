"""Setup cost of one Selenium test, split in two parts.

"browser" is starting a new session (what the tool controls); "navigation" is loading
the application, which depends mostly on the network.
"""

import json
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "selenium"))

from driver_factory import create_driver  # noqa: E402  pylint: disable=wrong-import-position
from pages.todo_page import TodoPage  # noqa: E402  pylint: disable=wrong-import-position

ITERATIONS = 10


def main():
    browser_start = []
    navigation = []
    for _ in range(ITERATIONS):
        start = time.perf_counter()
        driver = create_driver()
        try:
            browser_start.append(time.perf_counter() - start)
            start = time.perf_counter()
            TodoPage(driver).navigate()
            navigation.append(time.perf_counter() - start)
            version = driver.capabilities["browserVersion"]
        finally:
            driver.quit()
    result = {
        "browser_start": statistics.median(browser_start),
        "navigation": statistics.median(navigation),
        "version": version,
        "iterations": ITERATIONS,
    }
    sys.stdout.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    main()
