import json

import pytest

from tools import data_files
from tools.data_files import DataFileError, load_customer_data, load_order_cases, load_workflow_data

HEADER = ",".join(data_files.ORDER_COLUMNS)
ROW = (
    "simple_single_item,simple,\"[{'name': 'Notebook', 'price': 12.50, 'quantity': 1, 'weight': 0}]\","
    "regular,NONE,0,false,,12.50,0.00,1.00,0.00,13.50,"
)
ERROR_ROW = "empty_order,complex,[],regular,NONE,0,false,,,,,,,An order needs at least one item"
VALID_CUSTOMER_CASE = {
    "test_name": "valid_customer",
    "category": "valid",
    "customer": {"email": "a@example.com"},
    "expected": {"is_valid": True, "errors": []},
}
VALID_WORKFLOW = {
    "name": "flow",
    "gateway": {"available_credit": 10},
    "steps": [{"action": "calculate_total", "expected_error": "No order has been created"}],
}


def write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def problems_of(loader, path):
    with pytest.raises(DataFileError) as error:
        loader(path)
    return error.value.problems


@pytest.mark.parametrize(
    "rows, expected_problem",
    [
        pytest.param([ROW.replace(",simple,", ",basic,")], "orders.csv:2: category must be one of", id="bad_category"),
        pytest.param(
            [ROW, ROW.replace("13.50,", "13.00,")],
            "orders.csv:3: expected_total 13.0 does not add up to 13.5",
            id="total_does_not_add_up",
        ),
        pytest.param([ROW.replace("'price'", "price")], "orders.csv:2: items is not valid JSON", id="items_not_json"),
        pytest.param(
            [ROW.replace('"[{', '"{').replace('}]"', '}"')],
            "orders.csv:2: items must be a list of objects",
            id="items_not_a_list",
        ),
        pytest.param(
            [ROW.replace("12.50, ", "'12.50', ")],
            "orders.csv:2: item 'Notebook': price must be a number",
            id="item_price_is_text",
        ),
        pytest.param(
            [ROW.replace("'name': 'Notebook', ", "")], "orders.csv:2: every item needs a name", id="item_without_name"
        ),
        pytest.param(
            [ROW.replace(",regular,NONE,0,", ",regular,NONE,ten,")],
            "distance_km must be a number, got 'ten'",
            id="distance_is_text",
        ),
        pytest.param(
            [ROW.replace(",false,", ",yes,")], "is_express must be one of true, false", id="express_not_boolean"
        ),
        pytest.param(
            [ROW.replace(",false,,", ",false,01/11/2026,")], "order_date must be a YYYY-MM-DD date", id="date_not_iso"
        ),
        pytest.param([ROW.replace("simple_single_item,", ",")], "orders.csv:2: test_name is required", id="blank_name"),
        pytest.param(
            [ROW.replace(",13.50,", ",13.50,Some error")],
            "a row with expected_error must leave the expected amounts empty",
            id="error_row_with_amounts",
        ),
        pytest.param([ROW, ROW], "orders.csv: duplicate test name 'simple_single_item'", id="duplicate_name"),
    ],
)
def test_load_order_cases_invalid_row_reports_line_and_reason(tmp_path, rows, expected_problem):
    path = write(tmp_path, "orders.csv", "\n".join([HEADER, *rows]) + "\n")

    problems = problems_of(load_order_cases, path)

    assert any(expected_problem in problem for problem in problems), problems


def test_load_order_cases_missing_column_reports_header_line(tmp_path):
    path = write(tmp_path, "orders.csv", HEADER.replace(",expected_error", "") + "\n")

    assert problems_of(load_order_cases, path) == ["orders.csv:1: missing columns: expected_error"]


def test_load_order_cases_error_row_allows_invalid_item_values(tmp_path):
    path = write(tmp_path, "orders.csv", f"{HEADER}\n{ERROR_ROW}\n")

    cases = load_order_cases(path)

    assert [(case.expected, case.expected_error) for case in cases] == [(None, "An order needs at least one item")]


def customer_document(*cases, reference_date="2026-11-01"):
    return json.dumps({"reference_date": reference_date, "cases": list(cases)}, indent=2)


@pytest.mark.parametrize(
    "document, expected_problem",
    [
        pytest.param("[]", "expected an object with a 'cases' list", id="top_level_list"),
        pytest.param(customer_document(), "'cases' must be a non-empty list", id="no_cases"),
        pytest.param(
            customer_document(VALID_CUSTOMER_CASE, reference_date="soon"),
            "reference_date must be a",
            id="bad_reference_date",
        ),
        pytest.param(customer_document("valid_customer"), "case 0: must be an object", id="case_not_object"),
        pytest.param(
            customer_document({**VALID_CUSTOMER_CASE, "test_name": " "}),
            "test_name must be a non-empty",
            id="blank_name",
        ),
        pytest.param(
            customer_document({**VALID_CUSTOMER_CASE, "category": "misc"}), "category must be one of", id="bad_category"
        ),
        pytest.param(
            customer_document({**VALID_CUSTOMER_CASE, "customer": []}),
            "customer must be an object",
            id="customer_not_object",
        ),
        pytest.param(
            customer_document({**VALID_CUSTOMER_CASE, "expected": {"is_valid": "yes", "errors": []}}),
            "expected.is_valid must be true or false",
            id="is_valid_not_boolean",
        ),
        pytest.param(
            customer_document({**VALID_CUSTOMER_CASE, "expected": {"is_valid": True, "errors": "none"}}),
            "expected.errors must be a list of strings",
            id="errors_not_list",
        ),
        pytest.param(
            customer_document({**VALID_CUSTOMER_CASE, "expected": {"is_valid": True, "errors": ["Oops"]}}),
            "true exactly when expected.errors is empty",
            id="is_valid_contradicts_errors",
        ),
        pytest.param(
            customer_document(VALID_CUSTOMER_CASE, VALID_CUSTOMER_CASE), "duplicate test name", id="duplicate_name"
        ),
    ],
)
def test_load_customer_data_invalid_document_reports_reason(tmp_path, document, expected_problem):
    path = write(tmp_path, "customers.json", document)

    problems = problems_of(load_customer_data, path)

    assert any(expected_problem in problem for problem in problems), problems


def test_load_customer_data_invalid_case_reports_its_line(tmp_path):
    incomplete = {key: value for key, value in VALID_CUSTOMER_CASE.items() if key != "expected"}
    path = write(tmp_path, "customers.json", customer_document(VALID_CUSTOMER_CASE, incomplete))

    assert problems_of(load_customer_data, path) == ["customers.json:15: case 1: missing field 'expected'"]


def test_load_customer_data_broken_json_reports_its_line(tmp_path):
    path = write(tmp_path, "customers.json", '{\n  "reference_date": "2026-11-01",\n  "cases": [,]\n}\n')

    assert problems_of(load_customer_data, path) == ["customers.json:3: invalid JSON: Expecting value"]


def workflow_document(*workflows):
    return json.dumps({"reference_date": "2026-11-01", "workflows": list(workflows)}, indent=2)


def with_step(**step):
    return {**VALID_WORKFLOW, "steps": [step]}


@pytest.mark.parametrize(
    "document, expected_problem",
    [
        pytest.param(workflow_document(), "'workflows' must be a non-empty list", id="no_workflows"),
        pytest.param(workflow_document("flow"), "workflow 0: must be an object", id="workflow_not_object"),
        pytest.param(
            workflow_document({**VALID_WORKFLOW, "name": ""}), "name must be a non-empty string", id="blank_name"
        ),
        pytest.param(
            workflow_document({**VALID_WORKFLOW, "gateway": {"available_credit": -1}}),
            "gateway.available_credit must be a number of at least 0",
            id="negative_credit",
        ),
        pytest.param(
            workflow_document({**VALID_WORKFLOW, "steps": []}), "steps must be a non-empty list", id="no_steps"
        ),
        pytest.param(
            workflow_document({**VALID_WORKFLOW, "steps": ["pay"]}), "step 0: must be an object", id="step_not_object"
        ),
        pytest.param(
            workflow_document(with_step(action="refund", expected={})),
            "step 0: action must be one of",
            id="unknown_action",
        ),
        pytest.param(
            workflow_document(with_step(action="calculate_total", data=[], expected={})),
            "step 0: data must be an object",
            id="data_not_object",
        ),
        pytest.param(
            workflow_document(with_step(action="calculate_total", expected={}, expected_error="x")),
            "needs exactly one of 'expected'",
            id="expected_and_error",
        ),
        pytest.param(
            workflow_document(VALID_WORKFLOW, VALID_WORKFLOW), "duplicate test name 'flow'", id="duplicate_name"
        ),
    ],
)
def test_load_workflow_data_invalid_document_reports_reason(tmp_path, document, expected_problem):
    path = write(tmp_path, "workflows.json", document)

    problems = problems_of(load_workflow_data, path)

    assert any(expected_problem in problem for problem in problems), problems


def test_load_workflow_data_invalid_workflow_reports_its_line(tmp_path):
    path = write(tmp_path, "workflows.json", workflow_document(VALID_WORKFLOW, {**VALID_WORKFLOW, "steps": []}))

    assert problems_of(load_workflow_data, path) == ["workflows.json:16: workflow 1: steps must be a non-empty list"]


def test_main_committed_data_files_all_pass(capsys):
    exit_code = data_files.main()

    assert (exit_code, capsys.readouterr().out.count("OK ")) == (0, 5)


def test_main_invalid_data_file_is_reported(tmp_path, monkeypatch, capsys):
    for name in ("order_calculations.csv", "order_comparison.csv", "generated_orders.csv"):
        write(tmp_path, name, f"{HEADER}\n{ROW}\n")
    write(tmp_path, "customer_validation.json", customer_document(VALID_CUSTOMER_CASE))
    write(tmp_path, "order_workflows.json", workflow_document({**VALID_WORKFLOW, "steps": []}))
    monkeypatch.setattr(data_files, "TEST_DATA_DIR", tmp_path)

    exit_code = data_files.main()

    assert (exit_code, "INVALID order_workflows.json" in capsys.readouterr().out) == (1, True)
