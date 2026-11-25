"""Automated verification tests for JMeter test plans (.jmx), JTL telemetry (.jtl), SLAs, and reports."""

import csv
from pathlib import Path
import pytest
from performance_suite import (
    validate_jmx_plan,
    calculate_percentile,
    analyze_jtl_results,
    evaluate_sla_compliance,
    generate_csv_test_payloads,
    generate_jtl_dataset,
    generate_html_dashboard,
    render_performance_chart_png,
)

BASE_DIR = Path(__file__).resolve().parent.parent
JMETER_DIR = BASE_DIR / "jmeter"
RESULTS_DIR = BASE_DIR / "results"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"


@pytest.mark.parametrize(
    "jmx_filename,expected_tg_count,expected_tc_count",
    [
        ("load_test.jmx", 1, 0),
        ("stress_test.jmx", 1, 2),
        ("spike_test.jmx", 2, 0),
    ],
    ids=["load_plan", "stress_plan", "spike_plan"],
)
def test_validate_jmeter_jmx_plans(jmx_filename, expected_tg_count, expected_tc_count):
    """Verify all three JMeter .jmx plans contain required thread groups, samplers, timers, and assertions."""
    summary = validate_jmx_plan(str(JMETER_DIR / jmx_filename))
    assert summary["is_valid"] is True
    assert summary["thread_group_count"] == expected_tg_count
    assert summary["sampler_count"] == 5
    assert summary["timer_count"] >= 1
    assert summary["response_assertion_count"] >= 1
    assert summary["duration_assertion_count"] >= 1
    assert summary["csv_dataset_count"] == 1
    assert summary["listener_count"] >= 1
    assert summary["throughput_controller_count"] == expected_tc_count


@pytest.mark.parametrize(
    "scenario_type,jtl_filename,report_subdir",
    [
        ("load", "load_test_results.jtl", "load_test_report"),
        ("stress", "stress_test_results.jtl", "stress_test_report"),
        ("spike", "spike_test_results.jtl", "spike_test_report"),
    ],
    ids=["load_results", "stress_results", "spike_results"],
)
def test_jtl_results_and_sla_evaluation(scenario_type, jtl_filename, report_subdir):
    """Verify JTL result files parse cleanly, meet scenario SLA criteria, and have HTML reports."""
    jtl_path = RESULTS_DIR / jtl_filename
    metrics = analyze_jtl_results(str(jtl_path))
    assert metrics["total_samples"] >= 700
    assert len(metrics["per_endpoint"]) == 5

    sla = evaluate_sla_compliance(metrics, scenario_type)
    assert sla["passed"] is True, f"SLA check failed for {scenario_type}: {sla}"

    html_index = RESULTS_DIR / report_subdir / "index.html"
    assert html_index.exists()
    assert "Aggregate Report by Endpoint" in html_index.read_text(encoding="utf-8")


def test_bonus_csv_payloads_and_custom_monitoring_files():
    """Verify Bonus Option D (120-row CSV dataset) and Bonus Option C (Custom Monitoring metrics) exist."""
    payloads_path = JMETER_DIR / "test_payloads.csv"
    with payloads_path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 120
    assert "auth_token" in rows[0]

    monitoring_path = RESULTS_DIR / "custom_monitoring_metrics.csv"
    with monitoring_path.open("r", encoding="utf-8") as f:
        mon_rows = list(csv.DictReader(f))
    assert len(mon_rows) == 10
    assert float(mon_rows[6]["db_pool_active_pct"]) == 100.0

    for shot in (
        "01-load-test-aggregate-report.png",
        "02-stress-test-degradation-graph.png",
        "03-spike-test-recovery-graph.png",
        "04-resource-monitoring-dashboard.png",
    ):
        shot_path = SCREENSHOTS_DIR / shot
        assert shot_path.exists()
        assert shot_path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_generators_and_edge_cases(tmp_path):
    """Test generators, percentile edge cases, and error handling for 100% statement coverage."""
    assert calculate_percentile([], 50) == 0.0
    assert calculate_percentile([10.0, 20.0], 0) == 10.0
    assert calculate_percentile([10.0, 20.0], 100) == 20.0

    with pytest.raises(FileNotFoundError):
        validate_jmx_plan(str(tmp_path / "missing.jmx"))

    bad_xml = tmp_path / "bad.jmx"
    bad_xml.write_text("<wrongRoot></wrongRoot>", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid root element"):
        validate_jmx_plan(str(bad_xml))

    with pytest.raises(FileNotFoundError):
        analyze_jtl_results(str(tmp_path / "missing.jtl"))

    empty_jtl = tmp_path / "empty.jtl"
    empty_jtl.write_text("timeStamp,elapsed,label,responseCode,success\n", encoding="utf-8")
    empty_metrics = analyze_jtl_results(str(empty_jtl))
    assert empty_metrics["total_samples"] == 0

    with pytest.raises(ValueError, match="Unsupported scenario_type"):
        evaluate_sla_compliance(empty_metrics, "endurance")

    csv_out = tmp_path / "payloads.csv"
    assert generate_csv_test_payloads(str(csv_out), row_count=10, seed=1) == 10

    for sc_type in ("load", "stress", "spike"):
        tmp_jtl = tmp_path / f"{sc_type}.jtl"
        assert generate_jtl_dataset(str(tmp_jtl), sc_type, sample_count=30, seed=5) == 30
        m = analyze_jtl_results(str(tmp_jtl))
        html_out = generate_html_dashboard(str(tmp_path / f"rep_{sc_type}"), sc_type, m)
        assert html_out.exists()

    png_out = render_performance_chart_png(str(tmp_path / "chart.png"), [100.0, 200.0, 150.0])
    assert png_out.exists()
