from data_loader import DATA_DIR
from src.data_validator import validate_customers_json, validate_orders_csv

HEADER = ("test_name,items,customer_type,discount_code,distance_km,is_express,"
          "expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total\n")


def test_real_data_files_are_valid():
    assert validate_orders_csv(DATA_DIR / "order_calculations.csv") == []
    assert validate_orders_csv(DATA_DIR / "generated_orders.csv") == []
    assert validate_customers_json(DATA_DIR / "customer_validation.json") == []


def test_reports_line_numbers_for_bad_rows(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text(
        HEADER
        + "ok,\"[{'name':'A','price':1,'quantity':1,'weight':0}]\",regular,NONE,0,false,1,0,0.08,0,1.08\n"
        + "bad,\"[{'name':'A'}]\",vip,NONE,abc,maybe,1,0,0.08,0,1.08\n",
        encoding="utf-8",
    )
    errors = validate_orders_csv(bad)
    assert errors and all(e.startswith("Line 3") for e in errors)
    assert any("customer_type" in e for e in errors)
    assert any("distance_km" in e for e in errors)


def test_missing_columns_and_duplicates(tmp_path):
    no_cols = tmp_path / "a.csv"
    no_cols.write_text("foo,bar\n1,2\n", encoding="utf-8")
    assert "missing columns" in validate_orders_csv(no_cols)[0]

    dup = tmp_path / "b.csv"
    row = "x,[],regular,NONE,0,false,0,0,0,0,0\n"
    dup.write_text(HEADER + row + row, encoding="utf-8")
    assert any("duplicate" in e for e in validate_orders_csv(dup))


def test_customers_json_errors(tmp_path):
    broken = tmp_path / "broken.json"
    broken.write_text('[{"test_name": }]', encoding="utf-8")
    assert "invalid JSON" in validate_customers_json(broken)[0]

    wrong = tmp_path / "wrong.json"
    wrong.write_text('[{"test_name": "t", "customer": {}, "expected": {"is_valid": "yes"}}]', encoding="utf-8")
    assert len(validate_customers_json(wrong)) == 2

    root = tmp_path / "root.json"
    root.write_text("{}", encoding="utf-8")
    assert validate_customers_json(root) == ["Root must be a list"]