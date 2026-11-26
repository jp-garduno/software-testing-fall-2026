"""Bonus option B: time the same order tests written the traditional way and data-driven.

For 10, 50, 100 and 500 test cases the script writes two equivalent suites in
a temporary folder:

  - traditional: one test function per case, with the data written in the code
  - data-driven: one parametrized test that reads the cases from a CSV file

Each suite runs in its own pytest process, several times, and the median wall
time is kept. Two situations are measured, because they answer different
questions:

  - first run:  no bytecode cache for the suite, as on a CI server
  - repeat run: Python and pytest reuse the compiled suite, as on a developer's machine

Results go to performance/results.csv and performance/execution_time.png.

Run from the homework-7 directory:  python scripts/compare_performance.py
Add --chart-only to redraw the chart from results.csv without measuring again.
"""

import csv
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from matplotlib.figure import Figure

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "performance"

SUITE_SIZES = (10, 50, 100, 500)
REPETITIONS = 7
AMOUNTS = ("subtotal", "discount", "tax", "shipping", "total")

TRADITIONAL_HEADER = "from order_calculator import Order\n"

TRADITIONAL_TEST = '''

def test_{name}():
    order = Order({items}, "{customer_type}")
{apply_discount}    order.set_shipping({distance_km}, {is_express})

    assert order.calculate_total() == {expected}
'''

DATA_DRIVEN_SUITE = '''import pytest

from case_loaders import load_order_csv
from order_calculator import Order


@pytest.mark.parametrize("case", load_order_csv(r"{csv_path}"))
def test_order(case):
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance_km"], case["is_express"])

    assert order.calculate_total() == case["expected"]
'''

# Chart colours: two categorical hues checked for colour-blind separation,
# on a light surface with neutral ink for every label.
COLORS = {"traditional": "#2a78d6", "data-driven": "#eb6834"}
LABELS = {"traditional": "Traditional", "data-driven": "Data-driven"}
SURFACE, INK, INK_SOFT, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#e1e0d9", "#c3c2b7"


def repeated_cases(count):
    """Return `count` CSV rows: the 25 real cases, repeated with numbered names."""
    with open(ROOT / "test_data" / "order_calculations.csv", newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))
    cases = []
    for index in range(count):
        row = dict(rows[index % len(rows)])
        row["test_name"] = f"{row['test_name']}_{index + 1:03d}"
        cases.append(row)
    return cases


def traditional_suite(cases):
    """Write the cases as hard-coded test functions, one per case."""
    tests = []
    for row in cases:
        code = row["discount_code"]
        tests.append(
            TRADITIONAL_TEST.format(
                name=row["test_name"],
                items=json.loads(row["items"].replace("'", '"')),
                customer_type=row["customer_type"],
                apply_discount="" if code == "NONE" else f'    order.apply_discount("{code}")\n',
                distance_km=float(row["distance_km"]),
                is_express=row["is_express"] == "true",
                expected={amount: float(row[f"expected_{amount}"]) for amount in AMOUNTS},
            )
        )
    return TRADITIONAL_HEADER + "".join(tests)


def write_suites(folder, cases):
    """Create both suites in `folder`; return {approach: (test file, lines of test code)}."""
    csv_path = folder / "cases.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(cases[0]))
        writer.writeheader()
        writer.writerows(cases)

    sources = {
        "traditional": traditional_suite(cases),
        "data-driven": DATA_DRIVEN_SUITE.format(csv_path=csv_path),
    }
    suites = {}
    for approach, source in sources.items():
        test_file = folder / f"test_{approach.replace('-', '_')}.py"
        test_file.write_text(source, encoding="utf-8")
        suites[approach] = (test_file, len(source.splitlines()))
    return suites


def run_seconds(test_file, expected_tests, keep_cache):
    """Run one suite in a new pytest process and return how long the process took."""
    if not keep_cache:
        shutil.rmtree(test_file.parent / "__pycache__", ignore_errors=True)

    environment = dict(os.environ, PYTHONPATH=os.pathsep.join([str(ROOT / "src"), str(ROOT / "tests")]))
    command = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", test_file.name]

    started = time.perf_counter()
    run = subprocess.run(
        command, cwd=test_file.parent, env=environment, capture_output=True, text=True, check=False
    )
    elapsed = time.perf_counter() - started

    if f"{expected_tests} passed" not in run.stdout:
        raise RuntimeError(f"{test_file.name} did not pass {expected_tests} tests:\n{run.stdout}")
    return elapsed


def measure():
    """Time every suite size, approach and cache state; return one result per combination."""
    results = []
    with tempfile.TemporaryDirectory() as temporary:
        for size in SUITE_SIZES:
            folder = Path(temporary) / f"suite_{size}"
            folder.mkdir()
            suites = write_suites(folder, repeated_cases(size))

            for cache, keep_cache in (("first run", False), ("repeat run", True)):
                # The approaches take turns so a busy moment on the machine hits both.
                timings = {approach: [] for approach in suites}
                for _ in range(REPETITIONS):
                    for approach, (test_file, _) in suites.items():
                        timings[approach].append(run_seconds(test_file, size, keep_cache))

                for approach, (_, code_lines) in suites.items():
                    seconds = timings[approach]
                    results.append(
                        {
                            "cases": size,
                            "approach": approach,
                            "cache": cache,
                            "median_seconds": round(statistics.median(seconds), 3),
                            "min_seconds": round(min(seconds), 3),
                            "max_seconds": round(max(seconds), 3),
                            "test_code_lines": code_lines,
                        }
                    )
                    print(results[-1])
    return results


def save_csv(results):
    """Write the measurements as a table, the exact numbers behind the chart."""
    with open(RESULTS_DIR / "results.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)


def label_line_ends(panel, last_medians):
    """Write the value of the largest suite beside each line end.

    When both lines end at practically the same height their labels would sit
    on top of each other, so a single label is written for the two of them.
    """
    values = sorted(last_medians)
    if values[-1] - values[0] < 0.05:
        labels = [(statistics.mean(values), f"{values[0]:.2f}-{values[-1]:.2f} s (both)")]
    else:
        labels = [(value, f"{value:.2f} s") for value in values]

    for height, text in labels:
        panel.annotate(
            text,
            (SUITE_SIZES[-1], height),
            xytext=(9, 0),
            textcoords="offset points",
            va="center",
            color=INK,
            fontsize=9,
        )


def save_chart(results):
    """Draw one panel per cache state: run time against suite size, one line per approach."""
    figure = Figure(figsize=(10, 4.4), facecolor=SURFACE)
    panels = figure.subplots(1, 2, sharey=True)
    panel_titles = {
        "first run": "First run: nothing cached, as on a CI server",
        "repeat run": "Repeat run: compiled suite reused",
    }

    for panel, (cache, title) in zip(panels, panel_titles.items()):
        last_medians = []
        for approach, color in COLORS.items():
            rows = [row for row in results if row["cache"] == cache and row["approach"] == approach]
            medians = [float(row["median_seconds"]) for row in rows]
            last_medians.append(medians[-1])
            panel.plot(
                [int(row["cases"]) for row in rows],
                medians,
                color=color,
                linewidth=2,
                marker="o",
                markersize=8,
                markeredgecolor=SURFACE,
                markeredgewidth=2,
                label=LABELS[approach],
            )
        label_line_ends(panel, last_medians)

        panel.set_title(title, loc="left", color=INK, fontsize=10)
        panel.set_xlabel("Test cases in the suite", color=INK_SOFT, fontsize=9)
        panel.set_xticks(SUITE_SIZES)
        panel.set_xlim(-15, 720)
        panel.set_ylim(bottom=0)
        panel.set_facecolor(SURFACE)
        panel.grid(axis="y", color=GRID, linewidth=1)
        panel.set_axisbelow(True)
        panel.tick_params(colors=INK_SOFT, labelsize=9, length=0)
        for side in ("top", "right", "left"):
            panel.spines[side].set_visible(False)
        panel.spines["bottom"].set_color(AXIS)

    panels[0].set_ylabel("Median run time (seconds)", color=INK_SOFT, fontsize=9)
    figure.suptitle(
        "Same order tests, two ways of writing them: run time as the suite grows",
        x=0.06,
        ha="left",
        color=INK,
        fontsize=12,
    )
    figure.legend(
        *panels[0].get_legend_handles_labels(),
        loc="upper left",
        bbox_to_anchor=(0.055, 0.94),
        ncols=2,
        frameon=False,
        fontsize=9,
        labelcolor=INK_SOFT,
    )
    figure.tight_layout(rect=(0, 0, 1, 0.9))
    figure.savefig(RESULTS_DIR / "execution_time.png", dpi=150, facecolor=SURFACE)


def main():
    """Measure and save the table and the chart; `--chart-only` redraws from results.csv."""
    RESULTS_DIR.mkdir(exist_ok=True)
    if "--chart-only" in sys.argv:
        with open(RESULTS_DIR / "results.csv", newline="", encoding="utf-8") as csv_file:
            results = list(csv.DictReader(csv_file))
    else:
        results = measure()
        save_csv(results)
    save_chart(results)


if __name__ == "__main__":
    main()
