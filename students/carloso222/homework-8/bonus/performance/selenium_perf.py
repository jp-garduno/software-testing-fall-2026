"""Bonus C - performance metrics with Selenium.

Measures the same things as playwright/perf/performance.spec.js (browser start-up, page load and
each user operation) and writes bonus/performance/results/selenium.json.

Run from the homework-8 folder:  python bonus/performance/selenium_perf.py
"""

import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HOMEWORK_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HOMEWORK_DIR / "selenium"))

# pylint: disable=wrong-import-position
from pages.todo_page import TodoPage  # noqa: E402  # isort: skip
from support import settings  # noqa: E402  # isort: skip
from support.driver_factory import create_driver  # noqa: E402  # isort: skip

RUNS = int(os.getenv("PERF_RUNS", "5"))
BULK = 20
OUTPUT = Path(__file__).resolve().parent / "results" / "selenium.json"

NAVIGATION_TIMING_JS = """
const nav = performance.getEntriesByType('navigation')[0];
const fcp = performance.getEntriesByName('first-contentful-paint')[0];
return {ttfb: nav.responseStart, domContentLoaded: nav.domContentLoadedEventEnd,
        load: nav.loadEventEnd, fcp: fcp ? fcp.startTime : null};
"""


def timed(action) -> float:
    start = time.perf_counter()
    action()
    return round((time.perf_counter() - start) * 1000, 1)


def measure_setup() -> list[float]:
    times = []
    for _ in range(RUNS):
        start = time.perf_counter()
        driver = create_driver()
        times.append(round((time.perf_counter() - start) * 1000, 1))
        driver.quit()
    return times


def measure_page_load(driver) -> list[dict]:
    loads = []
    for _ in range(RUNS):
        driver.get("about:blank")
        wall = timed(
            lambda: driver.get(settings.BASE_URL)
        )  # get() returns after the load event
        loads.append({"wall": wall, **driver.execute_script(NAVIGATION_TIMING_JS)})
    return loads


def measure_operations(page: TodoPage) -> dict[str, list[float]]:
    ops: dict[str, list[float]] = {}
    bulk = [f"Bulk task {i + 1}" for i in range(BULK)]
    steps = [
        ("add_1_todo", lambda: page.add_todo("First task")),
        (f"add_{BULK}_todos", lambda: page.add_todos(*bulk)),
        ("toggle_1_todo", lambda: page.toggle_todo(0)),
        ("toggle_all", page.toggle_all),
        ("filter_active", page.filter_active),
        ("filter_completed", page.filter_completed),
        ("filter_all", page.filter_all),
        ("edit_1_todo", lambda: page.edit_todo(0, "Edited task")),
        ("delete_1_todo", lambda: page.delete_todo(0)),
        ("clear_completed", page.clear_completed),
    ]
    for _ in range(RUNS):
        page.reset()
        for name, action in steps:
            ops.setdefault(name, []).append(timed(action))
    return ops


def main() -> None:
    results = {"tool": "Selenium", "runs": RUNS, "setup": measure_setup()}
    # "normal": driver.get() waits for the load event, like Playwright's goto(waitUntil: "load").
    driver = create_driver(page_load_strategy="normal")
    try:
        caps = driver.capabilities
        results["browser"] = f"{caps.get('browserName')} {caps.get('browserVersion')}"
        results["pageLoad"] = measure_page_load(driver)
        results["operations"] = measure_operations(TodoPage(driver))
    finally:
        driver.quit()
    results["environment"] = {
        "os": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
        "baseUrl": settings.BASE_URL,
        "measuredAt": datetime.now(timezone.utc).isoformat(),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"Selenium performance results written to {OUTPUT}")


if __name__ == "__main__":
    main()
