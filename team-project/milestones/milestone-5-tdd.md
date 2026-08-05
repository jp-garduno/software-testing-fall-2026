# Milestone 5: TDD Feature

**Due**: End of Week 12  
**Points**: 15 (15% of project grade)  
**Focus**: Implement new feature using Test-Driven Development  
**Module Applied**: Test-Driven Development (Module 6)

---

## 🎯 Objectives

- Implement a complete feature using strict TDD
- Document Red-Green-Refactor cycles
- Show test-first development in git history
- Demonstrate TDD benefits and challenges
- Reflect on TDD process

---

## 📋 Deliverables

### 1. Feature Selection (10 points)

Choose **one substantial feature** to implement using TDD:

#### Option A: Shopping Cart Management (Recommended)

- Add item to cart
- Update quantity
- Remove item
- Calculate subtotal/total
- Apply discount codes
- Clear cart

#### Option B: Order Processing

- Create order from cart
- Validate order (stock, payment)
- Calculate shipping
- Apply tax
- Process payment
- Generate order confirmation

#### Option C: Search and Filtering

- Search products by keyword
- Filter by category, price range
- Sort results (price, rating, name)
- Pagination
- Search suggestions

#### Option D: Custom Feature

- Must be substantial (3-5 days of work)
- Clear testable requirements
- Not trivial (CRUD only is not sufficient)
- Requires instructor approval

---

### 2. TDD Implementation (50 points)

#### 2.1 Feature Specification

Create `docs/milestones/M5/feature-spec.md`:

```markdown
# Feature: Shopping Cart Management

## Requirements

### Functional Requirements

1. User can add product to cart

   - If product already in cart, increase quantity
   - Validate product exists and has stock
   - Maximum quantity per item: 10

2. User can update item quantity

   - Quantity must be between 1-10
   - Validate stock availability
   - Update cart total

3. User can remove item from cart

   - Item must exist in cart
   - Recalculate totals

4. Cart displays correct totals

   - Subtotal (sum of item prices)
   - Discount (if applicable)
   - Tax (based on location)
   - Total (subtotal - discount + tax)

5. User can apply discount code
   - Validate code exists and is active
   - Calculate discount (percentage or fixed)
   - One code per cart

### Acceptance Criteria

- [x] AC-1: Adding valid product increases cart size
- [x] AC-2: Adding duplicate product increases quantity
- [x] AC-3: Cannot add out-of-stock product
- [x] AC-4: Quantity update validates stock
- [x] AC-5: Removing item recalculates total
- [x] AC-6: Totals are calculated correctly
- [x] AC-7: Discount code validation works
- [x] AC-8: Invalid discount code is rejected
```

#### 2.2 TDD Workflow - Red-Green-Refactor

**Cycle 1: Add Item to Empty Cart**

```python
# STEP 1: RED - Write failing test
def test_add_item_to_empty_cart():
    """Test adding first item to cart"""
    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Test Product", price=10.00)

    # Act
    cart.add_item(product, quantity=1)

    # Assert
    assert len(cart.items) == 1
    assert cart.items[0].product_id == 1
    assert cart.items[0].quantity == 1

# Run test: FAIL (ShoppingCart doesn't exist yet)
```

```python
# STEP 2: GREEN - Minimal code to pass
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        item = CartItem(product_id=product.id, quantity=quantity)
        self.items.append(item)

class CartItem:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

# Run test: PASS ✅
```

```python
# STEP 3: REFACTOR - Improve code (if needed)
# Code is simple enough, no refactoring yet
# Commit: "test: add test for adding item to empty cart"
# Commit: "feat: implement add_item to cart"
```

**Cycle 2: Add Duplicate Product (Increase Quantity)**

```python
# RED
def test_add_duplicate_product_increases_quantity():
    """Test adding same product twice increases quantity"""
    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Test Product", price=10.00)

    # Act
    cart.add_item(product, quantity=2)
    cart.add_item(product, quantity=3)

    # Assert
    assert len(cart.items) == 1  # Still one unique item
    assert cart.items[0].quantity == 5  # But quantity increased

# Run: FAIL (adds duplicate instead of increasing)
```

```python
# GREEN
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        # Check if product already in cart
        existing = self._find_item(product.id)
        if existing:
            existing.quantity += quantity
        else:
            item = CartItem(product_id=product.id, quantity=quantity)
            self.items.append(item)

    def _find_item(self, product_id):
        for item in self.items:
            if item.product_id == product_id:
                return item
        return None

# Run: PASS ✅
# Commit: "test: add test for duplicate product"
# Commit: "feat: increase quantity for duplicate products"
```

**Cycle 3: Validate Stock Availability**

```python
# RED
def test_add_item_exceeding_stock_raises_error():
    """Test cannot add more items than available stock"""
    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Limited Product", price=10.00, stock=3)

    # Act & Assert
    with pytest.raises(InsufficientStockError):
        cart.add_item(product, quantity=5)

# Run: FAIL (no stock validation)
```

```python
# GREEN
class ShoppingCart:
    def add_item(self, product, quantity):
        # Validate stock
        if quantity > product.stock:
            raise InsufficientStockError(
                f"Only {product.stock} items available"
            )

        existing = self._find_item(product.id)
        if existing:
            if existing.quantity + quantity > product.stock:
                raise InsufficientStockError(
                    f"Cannot add {quantity} more. Only {product.stock} available"
                )
            existing.quantity += quantity
        else:
            item = CartItem(product_id=product.id, quantity=quantity)
            self.items.append(item)

# Run: PASS ✅
# REFACTOR: Extract validation to separate method
class ShoppingCart:
    def add_item(self, product, quantity):
        self._validate_stock(product, quantity)
        # ...rest of code

    def _validate_stock(self, product, quantity):
        existing = self._find_item(product.id)
        total_quantity = quantity + (existing.quantity if existing else 0)
        if total_quantity > product.stock:
            raise InsufficientStockError(
                f"Insufficient stock. Available: {product.stock}"
            )

# Run: PASS ✅
# Commit: "test: add stock validation test"
# Commit: "feat: validate stock when adding to cart"
# Commit: "refactor: extract stock validation method"
```

Continue TDD cycles for **ALL feature requirements**!

---

### 3. Git History Documentation (25 points)

#### 3.1 Git History Requirements

**Each Red-Green-Refactor cycle must have 2-3 commits**:

1. **RED commit**: Add failing test

   ```bash
   git add tests/
   git commit -m "test(cart): add test for removing item from cart"
   ```

2. **GREEN commit**: Minimal implementation

   ```bash
   git add src/
   git commit -m "feat(cart): implement remove_item method"
   ```

3. **REFACTOR commit** (if applicable):
   ```bash
   git add src/
   git commit -m "refactor(cart): extract total calculation to method"
   ```

**Minimum**: 15-20 commits showing TDD workflow

#### 3.2 Commit Message Format

Use conventional commits:

```
test(scope): description of test added
feat(scope): description of feature implemented
refactor(scope): description of refactoring

Examples:
test(cart): add test for calculating cart subtotal
feat(cart): implement subtotal calculation
refactor(cart): simplify total calculation logic
test(cart): add test for applying discount code
feat(cart): implement discount code validation
```

#### 3.3 Branch Structure

```bash
# Create TDD feature branch
git checkout -b feature/tdd-shopping-cart

# Work in TDD cycles
# Commit after each RED, GREEN, REFACTOR

# When complete, create PR
git push -u origin feature/tdd-shopping-cart
```

---

### 4. TDD Documentation (15 points)

Create `docs/milestones/M5/tdd-process.md`:

```markdown
# TDD Process Documentation

## Feature: Shopping Cart Management

### TDD Cycles

#### Cycle 1: Add Item to Empty Cart

**Duration**: 20 minutes

**RED Phase**:

- Wrote test `test_add_item_to_empty_cart()`
- Test failed: `NameError: ShoppingCart not defined`
- Commit: [abc123]

**GREEN Phase**:

- Created `ShoppingCart` and `CartItem` classes
- Minimal implementation: add item to list
- Test passed ✅
- Commit: [def456]

**REFACTOR Phase**:

- No refactoring needed (simple code)

**Lessons Learned**:

- Starting with test clarified API design
- Kept implementation minimal

---

#### Cycle 2: Add Duplicate Product

**Duration**: 30 minutes

**RED Phase**:

- Test: Adding same product should increase quantity
- Test failed: Created duplicate cart items instead
- Commit: [ghi789]

**GREEN Phase**:

- Added `_find_item()` helper
- Check for existing item before adding
- Test passed ✅
- Commit: [jkl012]

**REFACTOR Phase**:

- Extracted finding logic to private method
- Added docstrings
- Commit: [mno345]

**Challenges**:

- Initially forgot to check for existing items
- Test caught this immediately

---

[Continue for ALL TDD cycles...]

### Summary

**Total Cycles**: 12
**Total Commits**: 24
**Time Spent**: 6 hours
**Tests Written First**: 12/12 (100%)

**Benefits Observed**:

1. Clearer requirements understanding
2. Caught edge cases early
3. Refactoring was safe with test coverage
4. API design improved through test writing

**Challenges Faced**:

1. Initial slowdown (took 2x longer)
2. Temptation to write code before tests
3. Sometimes wrote too much code in GREEN phase

**Would Use TDD Again?**
Yes, for complex logic. Maybe not for simple CRUD.
```

---

## 📤 Submission Instructions

### 1. Required Files

```
feature/tdd-shopping-cart/   (branch)
├── src/
│   └── cart/
│       ├── cart.py (or cart.ts)
│       └── models.py
├── tests/
│   └── test_cart.py (or cart.test.ts)
└── docs/milestones/M5/
    ├── feature-spec.md
    ├── tdd-process.md
    └── tdd-retrospective.md
```

### 2. Create Pull Request

```bash
git checkout -b feature/tdd-shopping-cart
# Complete TDD cycles (15-20 commits)
git push -u origin feature/tdd-shopping-cart
gh pr create --title "M5: Shopping Cart Feature (TDD)" \
  --body "Implemented shopping cart using strict TDD. See docs/milestones/M5/ for process documentation."
```

### 3. Submit on Canvas

- Pull Request URL
- Feature spec link
- TDD process documentation link
- Git history showing Red-Green-Refactor pattern

---

## 🎯 Grading Rubric

| Category               | Points | Criteria                                        |
| ---------------------- | ------ | ----------------------------------------------- |
| **Feature Selection**  | 10     | Appropriate scope, clear requirements           |
| **TDD Implementation** | 50     | Strict TDD followed, tests written first        |
| **Git History**        | 25     | Clear Red-Green-Refactor commits, 15-20 commits |
| **TDD Documentation**  | 15     | Process documented, lessons learned             |
| **Code Quality**       | 10     | Clean code, good refactoring                    |
| **Test Quality**       | 10     | Comprehensive tests, edge cases covered         |

**Total**: 120 points (20% bonus available)

**Bonus**:

- +5: Pair programming (documented in commits)
- +5: 100% coverage for TDD feature
- +5: Exceptional refactoring quality
- +5: Video demonstration of TDD process

**Requirements**:

- Tests must be written BEFORE implementation (STRICT)
- Minimum 15 commits showing TDD cycles (REQUIRED)
- Feature must be complete and working (REQUIRED)

**Deductions**:

- Test written after code: -10 points per instance (checked via git blame)
- < 15 commits: -3 points per missing commit
- No TDD documentation: -15 points
- Feature incomplete: -20 points
- Code-first (not test-first): -30 points

---

## ✅ Checklist

- [ ] Feature selected and specified
- [ ] All requirements written as acceptance criteria
- [ ] TDD branch created
- [ ] First test written (RED)
- [ ] Minimal code to pass test (GREEN)
- [ ] Code refactored (REFACTOR)
- [ ] Cycle repeated for all requirements
- [ ] 15-20 commits showing TDD workflow
- [ ] All tests passing
- [ ] Feature fully implemented
- [ ] TDD process documented
- [ ] Lessons learned documented
- [ ] Code reviewed by team
- [ ] PR created with detailed description

---

## 💡 Tips for Success

### TDD Discipline

1. **ALWAYS write test first** - No exceptions!
2. **Watch test fail** - Verify it fails for the right reason
3. **Write minimal code** - Just enough to pass
4. **Run all tests** - Ensure no regressions
5. **Refactor** - Improve code while tests are green
6. **Commit often** - Document your process

### Test Writing

1. **One behavior per test**
2. **Clear test names** - Describe what's being tested
3. **AAA pattern** - Arrange, Act, Assert
4. **Test edge cases** - Not just happy path
5. **Keep tests simple** - Tests should be easy to understand

### Implementation

1. **Resist over-engineering** - Let tests drive design
2. **Fake it till you make it** - Simplest solution first
3. **Triangulate** - Add test cases to force generalization
4. **Baby steps** - Small, incremental changes

### Refactoring

1. **Green bar first** - Only refactor when tests pass
2. **One refactoring at a time**
3. **Run tests after each change**
4. **Extract methods** - Keep functions small
5. **Remove duplication** - DRY principle

### Common Mistakes

- ❌ Writing code before test
- ❌ Writing too many tests at once
- ❌ Not watching test fail
- ❌ Writing too much code in GREEN phase
- ❌ Refactoring without green tests
- ❌ Not committing after each phase

---

## 📚 Resources

- [Module 6: TDD Theory](../../06-test-driven-development/theory/)
- [TDD Exercises](../../06-test-driven-development/exercises/)
- [Kent Beck - TDD by Example](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [Martin Fowler - Is TDD Dead?](https://martinfowler.com/articles/is-tdd-dead/)
- [Testing Guidelines](../guidelines/testing-guidelines.md)

---

## ❓ FAQ

**Q: Can I write some code first to "explore"?**  
A: No! That defeats the purpose. Explore with tests.

**Q: What if test is hard to write?**  
A: That's valuable feedback! Your design may need improvement.

**Q: How minimal is "minimal code"?**  
A: Just enough to make the test pass. You can even hard-code returns at first.

**Q: When do I refactor?**  
A: Only when tests are green. Refactoring means changing structure without changing behavior.

**Q: What if I accidentally write code first?**  
A: Delete it and start over with the test. Really!

**Q: Can my team help?**  
A: Yes! Pair programming is encouraged. Take turns being driver/navigator.

---

**TDD is a discipline that takes practice. Stick with it, even when it feels slower!** 🔴🟢🔧
