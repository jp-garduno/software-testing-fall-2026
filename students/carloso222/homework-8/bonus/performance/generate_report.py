"""Bonus C - builds PERFORMANCE_REPORT.md from results/selenium.json and results/playwright.json.

Run from the homework-8 folder:  python bonus/performance/generate_report.py
"""

import json
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
REPORT = HERE / "PERFORMANCE_REPORT.md"

OPERATION_LABELS = {
    "add_1_todo": "Add 1 todo",
    "add_20_todos": "Add 20 todos",
    "toggle_1_todo": "Complete 1 todo",
    "toggle_all": "Toggle all (21 todos)",
    "filter_active": "Filter: Active",
    "filter_completed": "Filter: Completed",
    "filter_all": "Filter: All",
    "edit_1_todo": "Edit 1 todo",
    "delete_1_todo": "Delete 1 todo",
    "clear_completed": "Clear completed (20 todos)",
}


def load(name: str) -> dict:
    return json.loads((RESULTS / f"{name}.json").read_text(encoding="utf-8"))


def stats(values: list[float]) -> tuple[float, float, float]:
    return statistics.mean(values), min(values), max(values)


def fmt(ms: float) -> str:
    return f"{ms:,.0f} ms" if ms >= 100 else f"{ms:,.1f} ms"


def ratio(selenium_ms: float, playwright_ms: float) -> str:
    if playwright_ms == 0:
        return "-"
    value = selenium_ms / playwright_ms
    return f"{value:.1f}x" + (
        " (Playwright faster)"
        if value > 1.05
        else " (Selenium faster)" if value < 0.95 else ""
    )


def setup_section(sel: dict, pw: dict) -> list[str]:
    s_avg, s_min, s_max = stats(sel["setup"])
    p_avg, p_min, p_max = stats(pw["setup"])
    return [
        "## 1. Browser start-up (setup time)",
        "",
        f"Time to launch the browser and get a page ready, {sel['runs']} launches each.",
        "",
        "| Tool | Average | Min | Max |",
        "| --- | --- | --- | --- |",
        f"| Selenium (`webdriver.Chrome()`) | {fmt(s_avg)} | {fmt(s_min)} | {fmt(s_max)} |",
        f"| Playwright (`launch()` + `newContext()` + `newPage()`) | {fmt(p_avg)} | {fmt(p_min)} | {fmt(p_max)} |",
        "",
        f"Selenium / Playwright: **{ratio(s_avg, p_avg)}**",
        "",
    ]


def page_load_section(sel: dict, pw: dict) -> list[str]:
    lines = [
        "## 2. Page load",
        "",
        "Run 1 is a cold load (empty cache); runs 2+ are warm loads in the same browser session.",
        "*Wall* is the time the tool's `get()`/`goto()` call took; the other columns come from the",
        "browser's Navigation Timing API, so they describe the app itself, not the tool.",
        "",
        "| Tool | Load | Wall | TTFB | DOMContentLoaded | load event | First Contentful Paint |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for data in (sel, pw):
        loads = data["pageLoad"]
        groups = [
            ("cold (run 1)", loads[:1]),
            (f"warm (avg of {len(loads) - 1})", loads[1:]),
        ]
        for label, group in groups:
            if not group:
                continue

            def avg(key, rows=group):
                values = [row[key] for row in rows if row.get(key) is not None]
                return fmt(statistics.mean(values)) if values else "n/a"

            lines.append(
                f"| {data['tool']} | {label} | {avg('wall')} | {avg('ttfb')} | {avg('domContentLoaded')} "
                f"| {avg('load')} | {avg('fcp')} |"
            )
    return lines + [""]


def operations_section(
    sel: dict, pw: dict
) -> tuple[list[str], list[tuple[str, float]]]:
    lines = [
        "## 3. User operations",
        "",
        f"Average of {sel['runs']} runs. Each time includes the action *and* waiting until the UI shows it.",
        "",
        "| Operation | Selenium avg | Playwright avg | Selenium / Playwright |",
        "| --- | --- | --- | --- |",
    ]
    ratios = []
    total_sel = total_pw = 0.0
    for key, label in OPERATION_LABELS.items():
        if key not in sel["operations"] or key not in pw["operations"]:
            continue
        s_avg = statistics.mean(sel["operations"][key])
        p_avg = statistics.mean(pw["operations"][key])
        total_sel += s_avg
        total_pw += p_avg
        ratios.append((label, s_avg / p_avg if p_avg else 0))
        lines.append(
            f"| {label} | {fmt(s_avg)} | {fmt(p_avg)} | {ratio(s_avg, p_avg)} |"
        )
    lines.append(
        f"| **Whole workflow** | **{fmt(total_sel)}** | **{fmt(total_pw)}** | **{ratio(total_sel, total_pw)}** |"
    )
    return lines + [""], ratios


def _warm_avg(data: dict, key: str) -> float | None:
    values = [row[key] for row in data["pageLoad"][1:] if row.get(key) is not None]
    return statistics.mean(values) if values else None


def key_findings(sel: dict, pw: dict, ratios: list[tuple[str, float]]) -> list[str]:
    """Conclusions computed from the numbers, so they stay true when the results are refreshed."""
    slowest = max(ratios, key=lambda item: item[1])
    fastest = min(ratios, key=lambda item: item[1])
    s_setup, p_setup = statistics.mean(sel["setup"]), statistics.mean(pw["setup"])
    faster_setup = "Playwright" if p_setup < s_setup else "Selenium"
    findings = [
        f"- Browser start-up: **{faster_setup}** is faster ({fmt(s_setup)} vs {fmt(p_setup)} on average).",
        f"- Largest gap between tools: **{slowest[0]}** (Selenium / Playwright = {slowest[1]:.1f}x).",
        f"- Smallest gap: **{fastest[0]}** ({fastest[1]:.1f}x).",
    ]
    s_dcl, p_dcl = _warm_avg(sel, "domContentLoaded"), _warm_avg(pw, "domContentLoaded")
    if s_dcl and p_dcl:
        similar = abs(s_dcl - p_dcl) / max(s_dcl, p_dcl) < 0.35
        verdict = (
            "similar, so the app itself loads equally fast with both tools"
            if similar
            else "different"
        )
        findings.append(
            f"- Warm DOMContentLoaded measured inside the browser: {fmt(s_dcl)} (Selenium) vs {fmt(p_dcl)} "
            f"(Playwright) - {verdict}."
        )
    findings.append(
        "- Differences in the operations come from the tools, not from the app: Selenium sends one HTTP "
        "WebDriver command per find/click/read and polls its explicit waits, while Playwright keeps one "
        "WebSocket connection open and waits with built-in auto-waiting."
    )
    return findings


def main() -> None:
    sel, pw = load("selenium"), load("playwright")
    lines = [
        "# Performance Report (Bonus C)",
        "",
        "> Generated by `bonus/performance/generate_report.py` from `results/selenium.json` and",
        "> `results/playwright.json`. Re-run `scripts/run_all.ps1` (or the two perf commands) to refresh it.",
        "",
        "## Environment",
        "",
        "| | Selenium | Playwright |",
        "| --- | --- | --- |",
        f"| Browser | {sel.get('browser', '?')} | {pw.get('browser', '?')} |",
        f"| OS | {sel['environment']['os']} | {pw['environment']['os']} |",
        f"| Runtime | Python {sel['environment']['python']} | Node {pw['environment']['node']} |",
        f"| URL | {sel['environment']['baseUrl']} | {pw['environment']['baseUrl']} |",
        f"| Measured at (UTC) | {sel['environment']['measuredAt'][:19]} | {pw['environment']['measuredAt'][:19]} |",
        "",
    ]
    lines += setup_section(sel, pw)
    lines += page_load_section(sel, pw)
    op_lines, ratios = operations_section(sel, pw)
    lines += op_lines
    lines += ["## 4. Key findings", ""] + key_findings(sel, pw, ratios) + [""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {REPORT}")


if __name__ == "__main__":
    main()
