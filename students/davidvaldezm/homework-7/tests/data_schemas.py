"""Schemas for the external test records."""

STRING = {"type": "string"}
NAME = {"type": "string", "minLength": 1}
NUMBER = {"type": "number"}
BOOLEAN = {"type": "boolean"}
NULLABLE_CODE = {"type": ["string", "null"]}
DATE = {"type": "string", "format": "date"}
MONEY_FIELDS = ("subtotal", "discount", "tax", "shipping", "total")


def record(required, optional=None):
    """Build a schema with named required and optional properties."""
    return {
        "type": "object",
        "required": list(required),
        "properties": {**required, **(optional or {})},
        "additionalProperties": False,
    }


def array(items, minimum=0):
    """Build an array schema with a minimum length."""
    return {"type": "array", "items": items, "minItems": minimum}


ITEM = record({"name": NAME, "price": NUMBER, "quantity": NUMBER, "weight": NUMBER})
ORDER_INPUT = {
    "items": array(ITEM),
    "customer_type": {"enum": ["new", "regular"]},
    "discount_code": NULLABLE_CODE,
    "distance_km": NUMBER,
    "is_express": BOOLEAN,
}
TOTALS = record(dict.fromkeys(MONEY_FIELDS, NUMBER))
ORDER_CASE = record(
    {
        "test_name": NAME,
        **ORDER_INPUT,
        "discount_applied": {"type": ["boolean", "null"]},
        "expected_error": {"type": ["string", "null"]},
        **{f"expected_{key}": {"type": ["number", "null"]} for key in MONEY_FIELDS},
    }
)
ORDER_CASE["oneOf"] = [
    {
        "properties": {
            "expected_error": {"type": "null"},
            **{f"expected_{key}": NUMBER for key in MONEY_FIELDS},
        }
    },
    {
        "properties": {
            "expected_error": NAME,
            **{f"expected_{key}": {"type": "null"} for key in MONEY_FIELDS},
        }
    },
]
CUSTOMER_CASE = record(
    {
        "test_name": NAME,
        "as_of": DATE,
        "customer": {},
        "expected": record({"is_valid": BOOLEAN, "errors": array(STRING)}),
    }
)
STEP_SCHEMAS = {
    "validate_customer": (
        record({"customer": {}}),
        record({"valid": BOOLEAN, "errors": array(STRING)}),
    ),
    "create_order": (
        record(
            {"items": ORDER_INPUT["items"]},
            {key: value for key, value in ORDER_INPUT.items() if key != "items"},
        ),
        record({"status": NAME}, {"error": STRING}),
    ),
    "calculate_total": (None, {"oneOf": [TOTALS, record({"status": NAME})]}),
    "process_payment": (None, record({"status": NAME}, {"amount": NUMBER})),
    "generate_confirmation": (
        None,
        record({"status": NAME}, {"order_id": NAME, "email": NAME, "total": NUMBER}),
    ),
}
WORKFLOW = record(
    {
        "name": NAME,
        "as_of": DATE,
        "order_id": NAME,
        "payment_responses": array(BOOLEAN),
        "expected_charges": array(NUMBER),
        "steps": array(
            {
                "oneOf": [
                    record(
                        {
                            "action": {"const": action},
                            "expected": expected_schema,
                            **(
                                {"data": input_schema}
                                if input_schema is not None
                                else {}
                            ),
                        }
                    )
                    for action, (input_schema, expected_schema) in STEP_SCHEMAS.items()
                ]
            },
            1,
        ),
    }
)
