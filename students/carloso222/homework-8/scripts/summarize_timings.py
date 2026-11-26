"""Builds reports/timing-summary.md from the reports written by scripts/run_all.ps1 / run_all.sh.

Inputs (all optional except the Selenium and Playwright reports):
  reports/selenium-junit.xml                  pytest --junitxml
  reports/playwright-results.json             Playwright, Chromium, default (parallel) workers
  reports/playwright-results-1worker.json     Playwright, Chromium, 1 worker (same conditions as Selenium)
  reports/playwright-results-chrome-1worker.json  Playwright, installed Google Chrome, 1 worker (same browser)
  reports/playwright-cross-browser.json       Playwright, Chromium + Firefox + WebKit (bonus B)
  reports/behave-junit/*.xml                  behave --junit
  reports/wall-clock.json                     wall-clock seconds of each command (written by run_all)
  bonus/performance/results/*.json            browser start-up times (bonus C)
"""

import json
import statistics
import xml.etree.ElementTree as ET
from pathlib import Path

HOMEWORK_DIR = Path(__file__).resolve().parents[1]
REPORTS = HOMEWORK_DIR / "reports"
PERF = HOMEWORK_DIR / "bonus" / "performance" / "results"
OUTPUT = REPORTS / "timing-summary.md"
STATUS_ICON = {"expected": "✅", "unexpected": "❌", "flaky": "⚠️", "skipped": "⏭️"}


def read_json(path: Path) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else None


def junit_summary(path: Path) -> dict | None:
    if not path.exists():
        return None
    root = ET.parse(path).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    cases = suite.findall("testcase")
    xfailed = sum(
        1
        for c in cases
        if c.find("skipped") is not None
        and "xfail" in (c.find("skipped").get("type", ""))
    )
    return {
        "tests": len(cases),
        "failed": int(suite.get("failures", 0)) + int(suite.get("errors", 0)),
        "xfailed": xfailed,
        "total": float(suite.get("time", 0)),
        "average": (
            statistics.mean(float(c.get("time", 0)) for c in cases) if cases else 0
        ),
    }


def behave_summary(folder: Path) -> dict | None:
    files = sorted(folder.glob("*.xml")) if folder.exists() else []
    if not files:
        return None
    cases, total, failed, skipped = [], 0.0, 0, 0
    for file in files:
        root = ET.parse(file).getroot()
        for suite in [root] if root.tag == "testsuite" else root.findall("testsuite"):
            total += float(suite.get("time", 0))
            failed += int(suite.get("failures", 0)) + int(suite.get("errors", 0))
            skipped += int(suite.get("skipped", 0))
            cases += suite.findall("testcase")
    return {
        "scenarios": len(cases),
        "failed": failed,
        "skipped": skipped,
        "total": total,
    }


def playwright_tests(report: dict) -> list[dict]:
    found = []

    def walk(suite, titles):
        for spec in suite.get("specs", []):
            for test in spec["tests"]:
                result = test["results"][-1] if test["results"] else {"duration": 0}
                found.append(
                    {
                        "title": " › ".join(titles + [spec["title"]]),
                        "project": test["projectName"],
                        "status": test["status"],
                        "expected_failure": test["expectedStatus"] == "failed",
                        "duration": result["duration"] / 1000,
                    }
                )
        for child in suite.get("suites", []):
            walk(child, titles + [child["title"]])

    for top in report["suites"]:
        walk(top, [])
    return found


def playwright_summary(report: dict | None) -> dict | None:
    if report is None:
        return None
    tests = playwright_tests(report)
    return {
        "tests": len(tests),
        "failed": sum(1 for t in tests if t["status"] == "unexpected"),
        "xfailed": sum(1 for t in tests if t["expected_failure"]),
        "total": report["stats"]["duration"] / 1000,
        "average": statistics.mean(t["duration"] for t in tests) if tests else 0,
        "workers": report["config"].get("metadata", {}).get("actualWorkers")
        or report["config"].get("workers"),
    }


def seconds(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.2f} s"


def perf_setup(tool: str) -> float | None:
    data = read_json(PERF / f"{tool}.json")
    return statistics.mean(data["setup"]) / 1000 if data else None


def comparison_table(
    columns: list[tuple[str, dict | None, str]], wall: dict | None
) -> list[str]:
    """columns: (header, summary, wall-clock key). Columns without a report are left out."""
    columns = [column for column in columns if column[1] is not None]

    def tests(summary):
        passed = summary["tests"] - summary["failed"] - summary["xfailed"]
        return (
            f"{summary['tests']} ({passed} passed, {summary['xfailed']} expected failure, "
            f"{summary['failed']} failed)"
        )

    def row(label, values):
        return f"| {label} | " + " | ".join(values) + " |"

    rows = [
        row("Metric", [header for header, _, _ in columns]),
        "| --- |" + " --- |" * len(columns),
        row("Tests", [tests(summary) for _, summary, _ in columns]),
        row(
            "Total execution time (reported by the runner)",
            [seconds(summary["total"]) for _, summary, _ in columns],
        ),
    ]
    if wall:
        rows.append(
            row(
                "Wall clock of the whole command",
                [seconds(wall.get(key)) for _, _, key in columns],
            )
        )
    rows.append(
        row(
            "Average per test (as reported for each test)",
            [seconds(summary["average"]) for _, summary, _ in columns],
        )
    )
    return rows


def cross_browser_table(report: dict | None) -> list[str]:
    if report is None:
        return ["_Cross-browser report not found (run `npm run test:cross-browser`)._"]
    tests = playwright_tests(report)
    projects = [
        p
        for p in ("chromium", "firefox", "webkit")
        if any(t["project"] == p for t in tests)
    ]
    titles = list(dict.fromkeys(t["title"] for t in tests))
    lines = [
        "| Test | " + " | ".join(projects) + " |",
        "| --- |" + " --- |" * len(projects),
    ]
    for title in titles:
        cells = []
        for project in projects:
            match = next(
                (t for t in tests if t["title"] == title and t["project"] == project),
                None,
            )
            if match is None:
                cells.append("-")
            else:
                icon = STATUS_ICON.get(match["status"], match["status"])
                note = (
                    " (expected failure)"
                    if match["expected_failure"] and match["status"] == "expected"
                    else ""
                )
                cells.append(f"{icon}{note} {match['duration']:.2f} s")
        lines.append(f"| {title} | " + " | ".join(cells) + " |")
    totals = []
    for project in projects:
        own = [t for t in tests if t["project"] == project]
        ok = sum(1 for t in own if t["status"] == "expected")
        totals.append(
            f"**{ok}/{len(own)} as expected, {sum(t['duration'] for t in own):.1f} s**"
        )
    lines.append("| **Total** | " + " | ".join(totals) + " |")
    return lines


def main() -> None:
    sel = junit_summary(REPORTS / "selenium-junit.xml")
    pwn = playwright_summary(read_json(REPORTS / "playwright-results.json"))
    pw1 = playwright_summary(read_json(REPORTS / "playwright-results-1worker.json"))
    pwc = playwright_summary(
        read_json(REPORTS / "playwright-results-chrome-1worker.json")
    )
    bdd = behave_summary(REPORTS / "behave-junit")
    wall = read_json(REPORTS / "wall-clock.json")

    lines = [
        "# Timing summary",
        "",
        "Generated by `scripts/summarize_timings.py`.",
        "",
        "## Selenium vs Playwright",
        "",
    ]
    workers = pwn["workers"] if pwn else "?"
    lines += comparison_table(
        [
            ("Selenium + Chrome (1 browser, serial)", sel, "selenium"),
            ("Playwright + Chrome, 1 worker", pwc, "playwright_chrome_1worker"),
            ("Playwright + bundled Chromium, 1 worker", pw1, "playwright_1worker"),
            (f"Playwright + bundled Chromium, {workers} workers", pwn, "playwright"),
        ],
        wall,
    )
    setup_sel, setup_pw = perf_setup("selenium"), perf_setup("playwright")
    if setup_sel is not None and setup_pw is not None:
        lines += [
            "",
            f"Setup time (browser start-up, average of the bonus C runs, installed Chrome): "
            f"Selenium {seconds(setup_sel)}, Playwright {seconds(setup_pw)}.",
        ]
    if bdd:
        lines += [
            "",
            "## BDD (Behave + Selenium)",
            "",
            f"{bdd['scenarios']} scenarios, {bdd['failed']} failed, {bdd['skipped']} skipped, "
            f"{bdd['total']:.2f} s (wall clock: {seconds(wall.get('behave') if wall else None)}).",
        ]
    lines += ["", "## Cross-browser matrix (Playwright, bonus B)", ""]
    lines += cross_browser_table(read_json(REPORTS / "playwright-cross-browser.json"))
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Timing summary written to {OUTPUT}")


if __name__ == "__main__":
    main()
