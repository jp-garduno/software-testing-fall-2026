"""Measure page load and UI operation latency, not server load capacity."""

import json
import statistics
import sys
from functools import partial
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "selenium"))
from pages.browser import create_driver  # pylint: disable=wrong-import-position
from pages.todo_page import TodoPage  # pylint: disable=wrong-import-position


def main():
    """Collect five independent browser sessions with verified operations."""
    samples = []
    for _ in range(5):
        driver = create_driver()
        try:
            todo = TodoPage(driver)
            sample = {}
            for name, action in [
                ("navigate", todo.navigate),
                ("add", partial(todo.add_todo, "Timed task")),
                ("complete", partial(todo.toggle_todo, 0)),
                ("delete", partial(todo.delete_todo, 0)),
            ]:
                start = perf_counter()
                action()
                sample[name + "_ms"] = (perf_counter() - start) * 1000
            sample["dom_content_loaded_ms"] = driver.execute_script(
                "return performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd"
            )
            samples.append(sample)
        finally:
            driver.quit()
    summary = {
        key: {
            "median": statistics.median(row[key] for row in samples),
            "min": min(row[key] for row in samples),
            "max": max(row[key] for row in samples),
        }
        for key in samples[0]
    }
    result = {
        "samples": samples,
        "summary_ms": summary,
        "browser": driver.capabilities["browserVersion"],
    }
    output = ROOT / "reports/live/performance.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
