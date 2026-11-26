"""
Bonus Test Suite - Tests for Data Generator, Data Validator, and Performance Benchmark.
"""

import os
import time
import tempfile
import pytest
from src.data_generator import generate_orders_to_csv, generate_single_order
from src.data_validator import (
    validate_order_calculations_csv,
    validate_customer_validation_json,
    validate_order_workflows_json,
)
from src.customer_validator import validate_expiration
from tests.test_order_traditional import (
    test_01_single_item, test_02_multiple_items, test_03_save10_valid,
    test_04_save10_below_min, test_05_save20_valid, test_06_newuser_valid,
    test_07_shipping_standard, test_08_shipping_express, test_09_freeship_discount,
    test_10_complex_combination
)
from tests.test_order_data_driven import load_10_comparison_cases, test_order_data_driven_comparison


def test_bonus_a_data_generator_single():
    """Verify single order generator produces valid structure."""
    order = generate_single_order(1, seed=123)
    assert "test_name" in order
    assert float(order["expected_subtotal"]) >= 0.0
    assert float(order["expected_total"]) >= float(order["expected_subtotal"]) - float(order["expected_discount"])


def test_bonus_a_data_generator_file_generation():
    """Verify programmatic generation of 100 orders into CSV."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_csv = os.path.join(tmpdir, "test_100_orders.csv")
        records = generate_orders_to_csv(tmp_csv, count=100, seed=42)
        assert len(records) == 100
        assert os.path.exists(tmp_csv)
        assert os.path.getsize(tmp_csv) > 1000

        # Validate generated CSV with validator
        errors = validate_order_calculations_csv(tmp_csv)
        assert errors == [], f"Generated CSV has validation errors: {errors}"


def test_bonus_c_data_validator_valid_files():
    """Verify test data validator returns no errors on valid repo files."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    calc_csv = os.path.join(base_dir, "test_data", "order_calculations.csv")
    cust_json = os.path.join(base_dir, "test_data", "customer_validation.json")
    wf_json = os.path.join(base_dir, "test_data", "order_workflows.json")

    assert validate_order_calculations_csv(calc_csv) == []
    assert validate_customer_validation_json(cust_json) == []
    assert validate_order_workflows_json(wf_json) == []


def test_bonus_c_data_validator_catches_all_defect_branches():
    """Verify data validator detects missing files and specific syntax/data defects."""
    assert "File not found" in validate_order_calculations_csv("nonexistent.csv")[0]
    assert "File not found" in validate_customer_validation_json("nonexistent.json")[0]
    assert "File not found" in validate_order_workflows_json("nonexistent.json")[0]

    with tempfile.TemporaryDirectory() as tmpdir:
        # Empty CSV
        empty_csv = os.path.join(tmpdir, "empty.csv")
        with open(empty_csv, "w") as f:
            f.write("")
        assert "empty or missing headers" in validate_order_calculations_csv(empty_csv)[0]

        # Missing header
        bad_hdr_csv = os.path.join(tmpdir, "bad_hdr.csv")
        with open(bad_hdr_csv, "w") as f:
            f.write("test_name,items\n")
        assert "Missing header column" in validate_order_calculations_csv(bad_hdr_csv)[0]

        # CSV with row errors
        bad_row_csv = os.path.join(tmpdir, "bad_row.csv")
        headers = [
            "test_name", "items", "customer_type", "discount_code",
            "distance_km", "is_express", "expected_subtotal",
            "expected_discount", "expected_tax", "expected_shipping", "expected_total"
        ]
        with open(bad_row_csv, "w") as f:
            f.write(",".join(headers) + "\n")
            f.write(",not_json,regular,NONE,abc,maybe,nan,0,0,0,0\n")
            f.write("test2,\"{'not': 'list'}\",regular,NONE,10,true,10,0,0,0,10\n")
            f.write("test3,\"[{'name': 'x'}]\",regular,NONE,10,true,10,0,0,0,10\n")

        row_errs = validate_order_calculations_csv(bad_row_csv)
        assert any("Empty 'test_name'" in e for e in row_errs)
        assert any("Invalid JSON in 'items'" in e for e in row_errs)
        assert any("'items' must be a JSON array" in e for e in row_errs)
        assert any("missing key" in e for e in row_errs)
        assert any("not a valid float" in e for e in row_errs)
        assert any("must be 'true' or 'false'" in e for e in row_errs)

        # Bad customer JSONs
        bad_cust_root = os.path.join(tmpdir, "bad_cust_root.json")
        with open(bad_cust_root, "w") as f:
            f.write("{}")
        assert "must be a list" in validate_customer_validation_json(bad_cust_root)[0]

        bad_cust_item = os.path.join(tmpdir, "bad_cust_item.json")
        with open(bad_cust_item, "w") as f:
            f.write('[{"test_name": "t1", "expected": {"is_valid": "not_bool", "errors": "not_list"}}]')
        cust_errs = validate_customer_validation_json(bad_cust_item)
        assert any("missing 'customer'" in e for e in cust_errs)
        assert any("expected.is_valid must be boolean" in e for e in cust_errs)
        assert any("expected.errors must be list" in e for e in cust_errs)

        # Bad workflows JSONs
        bad_wf_syntax = os.path.join(tmpdir, "bad_wf.json")
        with open(bad_wf_syntax, "w") as f:
            f.write("{invalid")
        assert "Invalid JSON" in validate_order_workflows_json(bad_wf_syntax)[0]

        bad_wf_root = os.path.join(tmpdir, "bad_wf_root.json")
        with open(bad_wf_root, "w") as f:
            f.write('{"workflows": []}')
        assert "at least 3 workflows" in validate_order_workflows_json(bad_wf_root)[0]

        bad_wf_steps = os.path.join(tmpdir, "bad_wf_steps.json")
        with open(bad_wf_steps, "w") as f:
            f.write('{"workflows": [{"name": "w1", "steps": []}, {"name": "w2", "steps": []}, {"name": "w3", "steps": []}]}')
        assert any("must have a non-empty 'steps' list" in e for e in validate_order_workflows_json(bad_wf_steps))


def test_validate_expiration_none():
    """Verify validate_expiration with None input."""
    assert validate_expiration(None) == ["Invalid expiration format"]


def test_bonus_b_performance_comparison_benchmark():
    """
    Performance Benchmark (Bonus Option B).
    Measures execution time between traditional hardcoded tests and data-driven tests.
    """
    traditional_funcs = [
        test_01_single_item, test_02_multiple_items, test_03_save10_valid,
        test_04_save10_below_min, test_05_save20_valid, test_06_newuser_valid,
        test_07_shipping_standard, test_08_shipping_express, test_09_freeship_discount,
        test_10_complex_combination,
    ]

    cases = load_10_comparison_cases()
    iterations = 50

    # Measure Traditional
    start_trad = time.perf_counter()
    for _ in range(iterations):
        for fn in traditional_funcs:
            fn()
    dur_trad = time.perf_counter() - start_trad

    # Measure Data-Driven
    start_dd = time.perf_counter()
    for _ in range(iterations):
        for case in cases:
            test_order_data_driven_comparison(*case)
    dur_dd = time.perf_counter() - start_dd

    assert dur_trad > 0
    assert dur_dd > 0
    print(f"\n[Benchmark] Traditional: {dur_trad:.4f}s | Data-Driven: {dur_dd:.4f}s for {iterations * 10} executions")
