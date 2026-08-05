# Homework 7: Data-Driven Test Suite

**Due**: End of Week 13  
**Points**: 110 (100 base + 10 bonus)

## Overview

Create a comprehensive data-driven test suite for an e-commerce order processing system. You will implement the system and create extensive test data in multiple formats (CSV, JSON) to test all functionality.

## Learning Objectives

- Design and implement data-driven tests
- Manage test data in external files
- Separate test logic from test data
- Scale test suites efficiently
- Compare data-driven vs traditional testing approaches

## Scenario: E-Commerce Order Processing

You are testing an order processing system that:

- Validates customer information
- Calculates order totals with taxes and discounts
- Applies shipping costs based on multiple factors
- Validates payment information
- Generates order confirmations

## Part 1: Order Calculator (40 points)

### Implementation Requirements

Create `order_calculator.py` (Python) OR `orderCalculator.js` (JavaScript) with the following functionality:

**Order Calculation Rules**:

1. **Subtotal**: Sum of all item prices × quantities
2. **Discounts**:
   - `SAVE10`: 10% off orders > $50
   - `SAVE20`: 20% off orders > $100
   - `FREESHIP`: Free shipping
   - `NEWUSER`: 15% off first order
   - Invalid/expired codes: No discount
3. **Tax**: 8% of (subtotal - discount)
4. **Shipping**:
   - Weight-based: $0.50 per kg
   - Distance-based: $0.10 per km
   - Express shipping: 1.5× base shipping cost
   - Free shipping if discount code `FREESHIP` applied
5. **Total**: Subtotal - discount + tax + shipping

### Python Implementation

**order_calculator.py**:

```python
from typing import List, Dict, Tuple
from datetime import datetime

class Order:
    def __init__(self, items: List[Dict], customer_type: str = "regular"):
        """
        Initialize order

        Args:
            items: List of {"name": str, "price": float, "quantity": int, "weight": float}
            customer_type: "new" or "regular"
        """
        self.items = items
        self.customer_type = customer_type
        self.discount_code = None
        self.shipping_distance = 0
        self.is_express = False

    def apply_discount(self, code: str) -> bool:
        """Apply discount code, return True if valid"""
        valid_codes = {
            "SAVE10": {"min_order": 50, "discount_pct": 0.10},
            "SAVE20": {"min_order": 100, "discount_pct": 0.20},
            "FREESHIP": {"min_order": 0, "discount_pct": 0},
            "NEWUSER": {"min_order": 0, "discount_pct": 0.15}
        }

        if code not in valid_codes:
            return False

        subtotal = self.calculate_subtotal()
        if subtotal < valid_codes[code]["min_order"]:
            return False

        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False):
        """Set shipping parameters"""
        self.shipping_distance = distance_km
        self.is_express = is_express

    def calculate_subtotal(self) -> float:
        """Calculate subtotal (sum of item prices)"""
        # TODO: Implement
        pass

    def calculate_discount(self) -> float:
        """Calculate discount amount"""
        # TODO: Implement
        pass

    def calculate_tax(self) -> float:
        """Calculate tax (8% of subtotal after discount)"""
        # TODO: Implement
        pass

    def calculate_shipping(self) -> float:
        """Calculate shipping cost"""
        # TODO: Implement
        pass

    def calculate_total(self) -> Dict[str, float]:
        """
        Calculate order total with breakdown

        Returns:
            {
                "subtotal": float,
                "discount": float,
                "tax": float,
                "shipping": float,
                "total": float
            }
        """
        # TODO: Implement
        pass
```

### JavaScript Implementation

**orderCalculator.js**:

```javascript
class Order {
  constructor(items, customerType = "regular") {
    this.items = items; // [{name, price, quantity, weight}]
    this.customerType = customerType;
    this.discountCode = null;
    this.shippingDistance = 0;
    this.isExpress = false;
  }

  applyDiscount(code) {
    // TODO: Implement
  }

  setShipping(distanceKm, isExpress = false) {
    this.shippingDistance = distanceKm;
    this.isExpress = isExpress;
  }

  calculateSubtotal() {
    // TODO: Implement
  }

  calculateDiscount() {
    // TODO: Implement
  }

  calculateTax() {
    // TODO: Implement
  }

  calculateShipping() {
    // TODO: Implement
  }

  calculateTotal() {
    // Returns {subtotal, discount, tax, shipping, total}
    // TODO: Implement
  }
}

module.exports = Order;
```

### Test Data Requirements

Create **test_data/order_calculations.csv** with at least 25 test cases covering:

**CSV Format**:

```csv
test_name,items,customer_type,discount_code,distance_km,is_express,expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total
simple_order,"[{name:Item1,price:50,quantity:1,weight:1}]",regular,NONE,10,false,50.00,0.00,4.00,5.50,59.50
```

**Test Categories** (minimum required):

1. **Simple orders** (no discounts/shipping): 3 cases
2. **Discount validation**: 5 cases
   - Valid codes at minimum thresholds
   - Codes below minimum order
   - Invalid codes
   - Multiple items with discounts
3. **Tax calculations**: 4 cases
4. **Shipping calculations**: 6 cases
   - Various weights and distances
   - Express vs standard
   - Free shipping code
5. **Complex orders**: 7 cases
   - Multiple items, discounts, and shipping
   - Edge cases (zero quantity, negative values)
   - Maximum values

### Test Implementation

**Python - test_order_calculator.py**:

```python
import pytest
import csv
import json
from order_calculator import Order

def load_order_test_data():
    """Load test data from CSV"""
    test_data = []
    with open('test_data/order_calculations.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse items JSON string
            items = json.loads(row['items'].replace("'", '"'))
            test_data.append((
                row['test_name'],
                items,
                row['customer_type'],
                row['discount_code'] if row['discount_code'] != 'NONE' else None,
                float(row['distance_km']),
                row['is_express'] == 'true',
                float(row['expected_subtotal']),
                float(row['expected_discount']),
                float(row['expected_tax']),
                float(row['expected_shipping']),
                float(row['expected_total'])
            ))
    return test_data

@pytest.mark.parametrize(
    "test_name,items,customer_type,discount_code,distance,is_express,"
    "exp_subtotal,exp_discount,exp_tax,exp_shipping,exp_total",
    load_order_test_data(),
    ids=lambda val: val if isinstance(val, str) and len(val) < 30 else ""
)
def test_order_calculation(test_name, items, customer_type, discount_code,
                           distance, is_express, exp_subtotal, exp_discount,
                           exp_tax, exp_shipping, exp_total):
    """Test order calculations with data from CSV"""
    # Create order
    order = Order(items, customer_type)

    # Apply discount if provided
    if discount_code:
        order.apply_discount(discount_code)

    # Set shipping
    order.set_shipping(distance, is_express)

    # Calculate
    result = order.calculate_total()

    # Verify all components
    assert result['subtotal'] == pytest.approx(exp_subtotal, rel=1e-2), \
        f"{test_name}: Subtotal mismatch"
    assert result['discount'] == pytest.approx(exp_discount, rel=1e-2), \
        f"{test_name}: Discount mismatch"
    assert result['tax'] == pytest.approx(exp_tax, rel=1e-2), \
        f"{test_name}: Tax mismatch"
    assert result['shipping'] == pytest.approx(exp_shipping, rel=1e-2), \
        f"{test_name}: Shipping mismatch"
    assert result['total'] == pytest.approx(exp_total, rel=1e-2), \
        f"{test_name}: Total mismatch"
```

**JavaScript - orderCalculator.test.js**:

```javascript
const Order = require("./orderCalculator");
const fs = require("fs");
const { parse } = require("csv-parse/sync");

// Load CSV test data
const csvData = fs.readFileSync("test-data/order-calculations.csv", "utf8");
const records = parse(csvData, { columns: true });

// Convert CSV to test cases
const testCases = records.map((row) => ({
  testName: row.test_name,
  items: JSON.parse(row.items.replace(/'/g, '"')),
  customerType: row.customer_type,
  discountCode: row.discount_code === "NONE" ? null : row.discount_code,
  distance: parseFloat(row.distance_km),
  isExpress: row.is_express === "true",
  expected: {
    subtotal: parseFloat(row.expected_subtotal),
    discount: parseFloat(row.expected_discount),
    tax: parseFloat(row.expected_tax),
    shipping: parseFloat(row.expected_shipping),
    total: parseFloat(row.expected_total),
  },
}));

test.each(testCases)(
  "Order calculation: $testName",
  ({ items, customerType, discountCode, distance, isExpress, expected }) => {
    const order = new Order(items, customerType);

    if (discountCode) {
      order.applyDiscount(discountCode);
    }

    order.setShipping(distance, isExpress);
    const result = order.calculateTotal();

    expect(result.subtotal).toBeCloseTo(expected.subtotal, 2);
    expect(result.discount).toBeCloseTo(expected.discount, 2);
    expect(result.tax).toBeCloseTo(expected.tax, 2);
    expect(result.shipping).toBeCloseTo(expected.shipping, 2);
    expect(result.total).toBeCloseTo(expected.total, 2);
  },
);
```

## Part 2: Customer Validation (30 points)

### Implementation

Create customer validation module that validates:

- Email format
- Phone number format (US: (XXX) XXX-XXXX)
- Billing address (street, city, state, zip)
- Credit card number (Luhn algorithm)
- Credit card expiration date

### Test Data

Create **test_data/customer_validation.json** with at least 30 test cases:

```json
[
  {
    "test_name": "valid_customer_all_fields",
    "customer": {
      "email": "john@example.com",
      "phone": "(555) 123-4567",
      "billing_address": {
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "zip": "10001"
      },
      "credit_card": {
        "number": "4532015112830366",
        "expiration": "12/2025",
        "cvv": "123"
      }
    },
    "expected": {
      "is_valid": true,
      "errors": []
    }
  },
  {
    "test_name": "invalid_email",
    "customer": {
      "email": "invalid-email",
      "phone": "(555) 123-4567",
      "billing_address": {...},
      "credit_card": {...}
    },
    "expected": {
      "is_valid": false,
      "errors": ["Invalid email format"]
    }
  }
]
```

### Test Categories (minimum):

1. **Valid customers**: 3 cases
2. **Invalid emails**: 4 cases
3. **Invalid phones**: 4 cases
4. **Invalid addresses**: 5 cases
5. **Invalid credit cards**: 8 cases
6. **Multiple validation errors**: 6 cases

## Part 3: Comparison Analysis (20 points)

### Traditional vs Data-Driven

Create two versions of the same test suite:

1. **test_order_traditional.py** or **orderTraditional.test.js**:

   - Write 10 test functions WITHOUT parameterization
   - Each test has hardcoded data

2. **test_order_data_driven.py** or **orderDataDriven.test.js**:
   - Same 10 tests using parameterization
   - Data loaded from CSV/JSON

### Comparison Report

Create **COMPARISON_REPORT.md** analyzing:

1. **Lines of Code**:

   - Count LOC for both approaches
   - Calculate reduction percentage

2. **Maintainability**:

   - How easy to add new test cases?
   - How easy to update existing tests?

3. **Readability**:

   - Which is easier to understand?
   - Which has better test organization?

4. **Coverage**:

   - How many scenarios tested?
   - Time to add 10 more test cases?

5. **Conclusion**:
   - When to use each approach?
   - Pros and cons of data-driven testing

## Part 4: Integration Tests (10 points)

Create **test_data/order_workflows.json** with end-to-end order workflows:

```json
{
  "workflows": [
    {
      "name": "complete_order_flow",
      "steps": [
        {
          "action": "validate_customer",
          "data": {...},
          "expected": {"valid": true}
        },
        {
          "action": "create_order",
          "data": {...},
          "expected": {"status": "created"}
        },
        {
          "action": "calculate_total",
          "expected": {"total": 125.50}
        },
        {
          "action": "process_payment",
          "expected": {"status": "success"}
        }
      ]
    }
  ]
}
```

Implement at least 3 complete workflows.

## Bonus: Advanced Features (+10 points)

Implement ANY TWO of the following:

### Option A: Data Generation (+5 points)

Create a data generator that produces valid test data:

- Generate 100 valid orders programmatically
- Use Faker library for realistic data
- Save to CSV for regression testing

### Option B: Performance Comparison (+5 points)

- Measure execution time: Traditional vs Data-Driven
- Test with 10, 50, 100, 500 test cases
- Create graphs showing performance
- Analyze results

### Option C: Data Validation (+5 points)

- Validate test data files before running tests
- Check for required fields
- Verify data types
- Report invalid data with line numbers

### Option D: Excel Integration (+5 points)

- Load test data from Excel (.xlsx)
- Support multiple sheets
- Different sheet for each test category
- Include sample Excel file

## Deliverables

### Required Files

**Implementation**:

- `order_calculator.py` OR `orderCalculator.js`
- `customer_validator.py` OR `customerValidator.js`

**Tests**:

- `test_order_calculator.py` OR `orderCalculator.test.js`
- `test_customer_validator.py` OR `customerValidator.test.js`
- `test_order_traditional.py` OR `orderTraditional.test.js`
- `test_order_data_driven.py` OR `orderDataDriven.test.js`
- `test_integration.py` OR `integration.test.js`

**Test Data**:

- `test_data/order_calculations.csv` (25+ cases)
- `test_data/customer_validation.json` (30+ cases)
- `test_data/order_workflows.json` (3+ workflows)

**Documentation**:

- `README.md` - Setup and running instructions
- `COMPARISON_REPORT.md` - Analysis of traditional vs data-driven
- `TEST_DATA_SPEC.md` - Test data format documentation

**Results**:

- `coverage_report.html` - Test coverage report
- `test_results.txt` - All tests passing

### Submission Format

```
homework-7/
├── src/
│   ├── order_calculator.py (or .js)
│   └── customer_validator.py (or .js)
├── tests/
│   ├── test_order_calculator.py (or .test.js)
│   ├── test_customer_validator.py (or .test.js)
│   ├── test_order_traditional.py (or .test.js)
│   ├── test_order_data_driven.py (or .test.js)
│   └── test_integration.py (or .test.js)
├── test_data/
│   ├── order_calculations.csv
│   ├── customer_validation.json
│   └── order_workflows.json
├── README.md
├── COMPARISON_REPORT.md
├── TEST_DATA_SPEC.md
├── coverage_report.html
├── test_results.txt
└── requirements.txt (or package.json)
```

## Grading Rubric

### Implementation (40 points)

- Order calculator correctness: 20 points
- Customer validator correctness: 15 points
- Code quality and structure: 5 points

### Test Data Quality (30 points)

- Order calculations CSV (25+ cases): 10 points
- Customer validation JSON (30+ cases): 12 points
- Workflow JSON (3+ workflows): 5 points
- Data organization and naming: 3 points

### Tests (20 points)

- Test implementation correctness: 10 points
- Data loading and parsing: 5 points
- Test coverage (>80%): 5 points

### Analysis (10 points)

- Comparison report quality: 5 points
- Traditional vs data-driven tests: 5 points

### Documentation (10 points)

- README clarity: 3 points
- Test data specification: 4 points
- Code comments: 3 points

### Bonus (10 points)

- Advanced features: up to 10 points

## Evaluation Criteria

- ✅ All tests pass
- ✅ Test coverage > 80%
- ✅ Minimum test case counts met
- ✅ Data-driven tests properly load external data
- ✅ Comparison analysis is thorough
- ✅ Code is well-documented
- ✅ Follows conventional commits

## Tips

1. Start with simple test cases, then add complex ones
2. Validate your test data format before running tests
3. Use clear, descriptive test names
4. Handle edge cases (zero, negative, null values)
5. Test error conditions, not just happy path
6. Use relative paths for test data files
7. Commit frequently with conventional commits

## Resources

- [pytest parametrize documentation](https://docs.pytest.org/en/stable/parametrize.html)
- [Jest test.each documentation](https://jestjs.io/docs/api#testeachtablename-fn-timeout)
- [CSV parsing in Python](https://docs.python.org/3/library/csv.html)
- [JSON in JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON)

## Questions?

Post questions in GitHub Discussions or office hours.

Good luck! 🚀
