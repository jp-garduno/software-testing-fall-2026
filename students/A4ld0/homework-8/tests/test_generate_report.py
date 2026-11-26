"""Unit tests for the comparison and performance report generation."""

import json
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
import unittest
from unittest.mock import patch

import generate_report


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(mkdtemp())
        self.addCleanup(rmtree, self.root)
        patcher = patch.object(generate_report, "ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        (self.root / "reports").mkdir()
        (self.root / "COMPARISON_REPORT.md").write_text(
            "Heading\n<!-- METRICS_START -->\nOld\n<!-- METRICS_END -->\nEnding",
            encoding="utf-8")
        (self.root / "PERFORMANCE_REPORT.md").write_text(
            "<!-- PERFORMANCE_START -->\nOld\n<!-- PERFORMANCE_END -->\n"
            "<!-- BROWSER_START -->\nOld\n<!-- BROWSER_END -->",
            encoding="utf-8")

    def write_metrics(self, name, data):
        (self.root / "reports" / name).write_text(json.dumps(data), encoding="utf-8")

    def comparison(self):
        return (self.root / "COMPARISON_REPORT.md").read_text(encoding="utf-8")

    def performance(self):
        return (self.root / "PERFORMANCE_REPORT.md").read_text(encoding="utf-8")

    def test_missing_metrics_stay_pending(self):
        generate_report.main()
        self.assertIn("| Total execution time (s) | Pending | Pending |", self.comparison())
        self.assertIn("| chrome | 15 | Pending | Pending | Pending execution |", self.performance())
        self.assertIn("Heading", self.comparison())
        self.assertIn("Ending", self.comparison())

    def test_comparison_and_operation_durations(self):
        selenium = {
            "total_seconds": 10,
            "passed": 1,
            "tests": [{"setup_seconds": 2, "operations": [
                {"operation": "add", "milliseconds": 100},
                {"operation": "add", "milliseconds": 200},
            ]}],
        }
        playwright = {
            "total_seconds": 5,
            "tests": [{"browser": "chrome", "status": "passed", "setup_seconds": 1,
                       "operations": [{"operation": "add", "milliseconds": 75}]}],
        }
        self.write_metrics("selenium-metrics.json", selenium)
        self.write_metrics("playwright-metrics.json", playwright)
        generate_report.main()
        self.assertIn("| Total execution time (s) | 10.000 | 5.000 |", self.comparison())
        self.assertIn("| Average setup time (s) | 2.000 | 1.000 |", self.comparison())
        self.assertIn("| Passed / attempted | 1 / 1 | 1 / 1 |", self.comparison())
        self.assertIn("| add | 150.000 | 75.000 |", self.performance())

    def test_mixed_browser_run_is_not_a_chrome_timing(self):
        self.write_metrics("playwright-metrics.json", {
            "total_seconds": 4,
            "tests": [{"browser": "chrome", "status": "passed"},
                      {"browser": "firefox", "status": "passed"}],
        })
        generate_report.main()
        self.assertIn("| Total execution time (s) | Pending | Pending |", self.comparison())

    def test_compatibility_matrix_includes_failures(self):
        self.write_metrics("playwright-cross-browser.json", {"tests": [
            *[{"browser": "chrome", "status": "passed", "test": str(i)} for i in range(15)],
            {"browser": "firefox", "status": "failed", "test": "create"},
            {"browser": "webkit", "status": "timedOut", "test": "edit"},
        ]})
        generate_report.main()
        self.assertIn("| chrome | 15 | 15 | 0 | Passed |", self.performance())
        self.assertIn("| firefox | 15 | 0 | 1 | Review results |", self.performance())
        self.assertIn("firefox failures: create", self.performance())
        self.assertIn("webkit failures: edit", self.performance())

    def test_empty_execution_has_no_average(self):
        report = {"total_seconds": 0.2, "tests": [], "passed": 0}
        self.write_metrics("selenium-metrics.json", report)
        generate_report.main()
        self.assertIn("| Average elapsed time per test (s) | Pending | Pending |",
                      self.comparison())
