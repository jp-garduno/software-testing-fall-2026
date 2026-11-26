"""Build reviewed fixtures: expected results are literals, not calls to the SUT."""

import csv
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "test_data"
FIELDS = [
    "test_name",
    "category",
    "items",
    "customer_type",
    "discount_code",
    "distance_km",
    "is_express",
    "expected_subtotal",
    "expected_discount",
    "expected_tax",
    "expected_shipping",
    "expected_total",
    "expected_error",
]


def item(price, quantity=1, weight=0):
    """Create a synthetic product."""
    return {
        "name": "Sample product",
        "price": price,
        "quantity": quantity,
        "weight": weight,
    }


def order(
    name,
    category,
    items,
    expected,
    code="NONE",
    **options,
):
    """Describe one golden pricing case, including invalid-input scenarios."""
    values = expected if expected != "ValueError" else [""] * 5
    return dict(
        zip(
            FIELDS,
            [
                name,
                category,
                json.dumps(items),
                options.get("customer", "regular"),
                code,
                options.get("distance", 0),
                str(options.get("express", False)).lower(),
                *values,
                "ValueError" if expected == "ValueError" else "",
            ],
        )
    )


ORDERS = [
    order("simple_one", "simple", [item(10)], [10, 0, 0.8, 0, 10.8]),
    order("simple_quantity", "simple", [item(12.5, 2)], [25, 0, 2, 0, 27]),
    order("simple_empty", "simple", [], [0, 0, 0, 0, 0]),
    order("save10_at_50", "discount", [item(50)], [50, 0, 4, 0, 54], "SAVE10"),
    order(
        "save10_above_50",
        "discount",
        [item(50.01)],
        [50.01, 5, 3.6, 0, 48.61],
        "SAVE10",
    ),
    order("save20_at_100", "discount", [item(100)], [100, 0, 8, 0, 108], "SAVE20"),
    order(
        "save20_above_100",
        "discount",
        [item(100.01)],
        [100.01, 20, 6.4, 0, 86.41],
        "SAVE20",
    ),
    order(
        "save10_below_50", "discount", [item(49.99)], [49.99, 0, 4, 0, 53.99], "SAVE10"
    ),
    order(
        "newuser_eligible",
        "discount",
        [item(80)],
        [80, 12, 5.44, 0, 73.44],
        "NEWUSER",
        customer="new",
    ),
    order(
        "newuser_returning", "discount", [item(80)], [80, 0, 6.4, 0, 86.4], "NEWUSER"
    ),
    order("invalid_code", "discount", [item(60)], [60, 0, 4.8, 0, 64.8], "INVALID"),
    order("expired_code", "discount", [item(70)], [70, 0, 5.6, 0, 75.6], "EXPIRED"),
    order("tax_one_cent", "tax", [item(0.01)], [0.01, 0, 0, 0, 0.01]),
    order("tax_rounds_up", "tax", [item(0.07)], [0.07, 0, 0.01, 0, 0.08]),
    order("tax_fractional", "tax", [item(19.99)], [19.99, 0, 1.6, 0, 21.59]),
    order("tax_fractional_unit", "tax", [item(0.0625, 4)], [0.25, 0, 0.02, 0, 0.27]),
    order(
        "shipping_standard",
        "shipping",
        [item(100, 1, 2)],
        [100, 0, 8, 2, 110],
        distance=10,
    ),
    order(
        "shipping_weight_quantity", "shipping", [item(10, 3, 2)], [30, 0, 2.4, 3, 35.4]
    ),
    order(
        "shipping_express",
        "shipping",
        [item(50, 1, 2)],
        [50, 0, 4, 3, 57],
        distance=10,
        express=True,
    ),
    order(
        "shipping_free",
        "shipping",
        [item(50, 1, 10)],
        [50, 0, 4, 0, 54],
        "FREESHIP",
        distance=100,
        express=True,
    ),
    order(
        "shipping_fractional",
        "shipping",
        [item(20, 1, 0.2)],
        [20, 0, 1.6, 0.15, 21.75],
        distance=0.5,
    ),
    order(
        "shipping_distance_only",
        "shipping",
        [item(10, 0, 4)],
        [0, 0, 0, 1, 1],
        distance=10,
    ),
    order(
        "complex_save20",
        "complex",
        [item(40, 2, 1), item(30, 1, 2)],
        [110, 22, 7.04, 4.5, 99.54],
        "SAVE20",
        distance=10,
        express=True,
    ),
    order(
        "complex_new",
        "complex",
        [item(20, 2, 0.5), item(40, 1, 2)],
        [80, 12, 5.44, 3.5, 76.94],
        "NEWUSER",
        customer="new",
        distance=20,
    ),
    order(
        "complex_large",
        "complex",
        [item(1000000, 100, 100)],
        [100000000, 20000000, 6400000, 6000, 86406000],
        "SAVE20",
        distance=10000,
    ),
    order(
        "complex_zero_quantity",
        "complex",
        [item(100, 0, 20), item(10, 2, 1)],
        [20, 0, 1.6, 1, 22.6],
        "SAVE10",
    ),
    order("complex_negative_price", "complex", [item(-1)], "ValueError"),
    order("complex_negative_quantity", "complex", [item(1, -1)], "ValueError"),
    order("complex_negative_weight", "complex", [item(1, 1, -1)], "ValueError"),
    order("complex_negative_distance", "complex", [item(1)], "ValueError", distance=-1),
    order(
        "complex_free_multi",
        "complex",
        [item(10, 2, 2), item(30, 1, 1)],
        [50, 0, 4, 0, 54],
        "FREESHIP",
        distance=100,
    ),
]

BASE_CUSTOMER = {
    "email": "ada@example.com",
    "phone": "(555) 123-4567",
    "billing_address": {
        "street": "123 Example St",
        "city": "Test City",
        "state": "NY",
        "zip": "10001",
    },
    "credit_card": {
        "number": "4242424242424242",
        "expiration": "12/2030",
        "cvv": "123",
    },
}


def customer_case(name, category, edits, errors):
    """Change explicit input fields while keeping literal expected errors."""
    customer = deepcopy(BASE_CUSTOMER)
    for path, value in edits.items():
        target = customer
        parts = path.split(".")
        for part in parts[:-1]:
            target = target[part]
        target[parts[-1]] = value
    return {
        "test_name": name,
        "category": category,
        "customer": customer,
        "expected": {"is_valid": not errors, "errors": errors},
    }


def build_customers():
    """Provide every required category, with a frozen November 2026 clock."""
    cases = [
        customer_case("valid_standard", "valid", {}, []),
        customer_case(
            "valid_current_month", "valid", {"credit_card.expiration": "11/2026"}, []
        ),
        customer_case(
            "valid_zip4_amex",
            "valid",
            {
                "billing_address.zip": "10001-1234",
                "credit_card.number": "378282246310005",
                "credit_card.cvv": "1234",
            },
            [],
        ),
    ]
    for index, value in enumerate(
        ["invalid", "a@@example.com", "a@example", "a b@example.com"]
    ):
        cases.append(
            customer_case(
                f"email_{index}", "email", {"email": value}, ["Invalid email format"]
            )
        )
    for index, value in enumerate(
        ["5551234567", "(55) 123-4567", "+1 (555) 123-4567", None]
    ):
        cases.append(
            customer_case(
                f"phone_{index}", "phone", {"phone": value}, ["Invalid phone format"]
            )
        )
    for index, (path, value, error) in enumerate(
        [
            ("street", "", "street"),
            ("city", "   ", "city"),
            ("state", "ZZ", "state"),
            ("zip", "1234", "zip"),
            ("zip", "ABCDE", "zip"),
        ]
    ):
        cases.append(
            customer_case(
                f"address_{index}",
                "address",
                {f"billing_address.{path}": value},
                [f"Invalid billing {error}"],
            )
        )
    for index, (field, value, message) in enumerate(
        [
            ("number", "4242424242424241", "number"),
            ("number", "123", "number"),
            ("number", "4242abcd42424242", "number"),
            ("number", "0000000000000000", "number"),
            ("expiration", "10/2026", "expiration"),
            ("expiration", "13/2030", "expiration"),
            ("expiration", "2030-12", "expiration"),
            ("cvv", "12", "CVV"),
        ]
    ):
        cases.append(
            customer_case(
                f"card_{index}",
                "card",
                {f"credit_card.{field}": value},
                [f"Invalid credit card {message}"],
            )
        )
    multiple = [
        (
            {"email": "bad", "phone": "bad"},
            ["Invalid email format", "Invalid phone format"],
        ),
        (
            {"billing_address.street": "", "billing_address.city": ""},
            ["Invalid billing street", "Invalid billing city"],
        ),
        (
            {"billing_address.state": "XX", "billing_address.zip": "0"},
            ["Invalid billing state", "Invalid billing zip"],
        ),
        (
            {"credit_card.number": "0", "credit_card.expiration": "01/2020"},
            ["Invalid credit card number", "Invalid credit card expiration"],
        ),
        (
            {"email": None, "credit_card.cvv": "abc"},
            ["Invalid email format", "Invalid credit card CVV"],
        ),
        (
            {"phone": "", "billing_address.zip": None, "credit_card.cvv": ""},
            ["Invalid phone format", "Invalid billing zip", "Invalid credit card CVV"],
        ),
    ]
    for index, (edits, errors) in enumerate(multiple):
        cases.append(customer_case(f"multiple_{index}", "multiple", edits, errors))
    return cases


def build_workflows():
    """Three complete flows plus two rejection paths, all with literal totals."""
    workflows = []
    for name, index in [
        ("regular_purchase", 0),
        ("new_customer_purchase", 23),
        ("free_shipping_purchase", 30),
    ]:
        row = ORDERS[index]
        data = {
            "items": json.loads(row["items"]),
            "customer_type": row["customer_type"],
            "discount_code": row["discount_code"],
            "distance_km": row["distance_km"],
            "is_express": row["is_express"] == "true",
        }
        total = row["expected_total"]
        workflows.append(
            {
                "name": name,
                "order_id": name,
                "payment_approved": True,
                "steps": [
                    {
                        "action": "validate_customer",
                        "data": BASE_CUSTOMER,
                        "expected": {"is_valid": True, "errors": []},
                    },
                    {
                        "action": "create_order",
                        "data": data,
                        "expected": {"status": "created"},
                    },
                    {
                        "action": "calculate_total",
                        "expected": {
                            key: row[f"expected_{key}"]
                            for key in (
                                "subtotal",
                                "discount",
                                "tax",
                                "shipping",
                                "total",
                            )
                        },
                    },
                    {"action": "process_payment", "expected": {"status": "success"}},
                    {
                        "action": "confirmation",
                        "expected": {
                            "status": "confirmed",
                            "order_id": name,
                            "total": total,
                        },
                    },
                    {
                        "action": "process_payment",
                        "expected": {"status": "already_paid"},
                    },
                ],
                "expected_payment_calls": [total],
            }
        )
    declined = deepcopy(workflows[0])
    declined.update(
        name="payment_declined", order_id="payment_declined", payment_approved=False
    )
    declined["steps"] = declined["steps"][:4] + [
        {"action": "confirmation", "expected": {"status": "unpaid"}}
    ]
    declined["steps"][3]["expected"] = {"status": "declined"}
    workflows.append(declined)
    invalid = deepcopy(BASE_CUSTOMER)
    invalid["email"] = "bad"
    workflows.append(
        {
            "name": "invalid_customer_blocked",
            "order_id": "blocked",
            "payment_approved": True,
            "steps": [
                {
                    "action": "validate_customer",
                    "data": invalid,
                    "expected": {"is_valid": False, "errors": ["Invalid email format"]},
                },
                {
                    "action": "create_order",
                    "data": {},
                    "expected": {"status": "blocked"},
                },
            ],
            "expected_payment_calls": [],
        }
    )
    return {"reference_date": "2026-11-10", "workflows": workflows}


def main():
    """Write deterministic CSV and JSON fixtures using standard encodings."""
    ROOT.mkdir(exist_ok=True)
    with (ROOT / "order_calculations.csv").open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(ORDERS)
    (ROOT / "customer_validation.json").write_text(
        json.dumps(build_customers(), indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / "order_workflows.json").write_text(
        json.dumps(build_workflows(), indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
