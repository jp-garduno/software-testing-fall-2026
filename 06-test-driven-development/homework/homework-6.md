# Homework 6: TDD Feature Development

**Module**: 6 - Test Driven Development  
**Due Date**: End of Week 11  
**Points**: 110 (100 base + 10 bonus)  
**Estimated Time**: 6-7 hours

---

## 🎯 Objectives

By completing this homework, you will:

- Master the Red-Green-Refactor TDD cycle
- Write tests before implementation code
- Design better code through test-first thinking
- Document TDD process with git commits
- Reflect on TDD benefits and challenges

---

## 📋 Assignment Overview

Build a **Library Management System** using **strict Test Driven Development**. You must write every test BEFORE implementing the corresponding code.

### System Components

1. **Book** - ISBN, title, author, available copies
2. **Member** - ID, name, borrowed books, borrow limit
3. **Library** - Catalog management, borrowing operations
4. **Search** - Find books by various criteria
5. **Late Fees** - Calculate fees for overdue books

---

## 🎯 Part 1: Core TDD Implementation (30 points)

### Requirements

Implement the following using **strict TDD**:

#### Book Class

- Properties: ISBN, title, author, total_copies, available_copies
- Methods: `is_available()`, `borrow()`, `return_copy()`
- Validation: ISBN must be 10 or 13 digits, title required

#### Member Class

- Properties: member_id, name, borrowed_books (list), max_borrow_limit (default 3)
- Methods: `can_borrow()`, `add_borrowed_book()`, `return_book()`
- Business rule: Cannot borrow more than limit

#### Library Class

- Methods:
  - `add_book(book)` - Add book to catalog
  - `register_member(member)` - Register new member
  - `borrow_book(member_id, isbn)` - Borrow a book
  - `return_book(member_id, isbn)` - Return a book
  - `search_by_title(title)` - Search books
  - `search_by_author(author)` - Search books
  - `get_available_books()` - List available books

### TDD Requirements

- Write test FIRST for every feature
- Minimum 25 tests total
- All tests must pass
- Follow Red-Green-Refactor cycle
- Git commit history must demonstrate TDD (see Part 2)

### Example Test Progression

**Python Example**:

```python
# Test 1: Book exists
def test_book_can_be_created():
    book = Book("1234567890", "Test Book", "Author")
    assert book.title == "Test Book"

# Test 2: Book has copies
def test_book_has_available_copies():
    book = Book("1234567890", "Test Book", "Author", copies=5)
    assert book.available_copies == 5

# Test 3: Can check availability
def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Test Book", "Author", copies=1)
    assert book.is_available() == True

# Continue with more tests...
```

**JavaScript Example**:

```javascript
describe("Book", () => {
  test("can be created with properties", () => {
    const book = new Book("1234567890", "Test Book", "Author");
    expect(book.title).toBe("Test Book");
  });

  test("has available copies", () => {
    const book = new Book("1234567890", "Test Book", "Author", 5);
    expect(book.availableCopies).toBe(5);
  });

  test("is available when copies exist", () => {
    const book = new Book("1234567890", "Test Book", "Author", 1);
    expect(book.isAvailable()).toBe(true);
  });
});
```

### Evaluation Criteria

| Criterion     | Points | Description                 |
| ------------- | ------ | --------------------------- |
| Functionality | 15     | All features work correctly |
| Test Coverage | 8      | >90% coverage achieved      |
| TDD Adherence | 7      | Tests written before code   |

---

## 📝 Part 2: TDD Process Documentation (25 points)

Document **5 complete Red-Green-Refactor cycles** in detail.

### Format for Each Cycle

````markdown
## Cycle #1: Book Availability Check

### RED Phase

**Test Written**:

```python
def test_book_not_available_when_no_copies():
    book = Book("1234567890", "Test", "Author", copies=0)
    assert book.is_available() == False
```
````

**Test Result**: FAIL - `is_available()` method doesn't exist

### GREEN Phase

**Code Written**:

```python
class Book:
    def __init__(self, isbn, title, author, copies=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.available_copies = copies

    def is_available(self):
        return self.available_copies > 0
```

**Test Result**: PASS - All tests green

### REFACTOR Phase

**Improvements Made**: None needed yet, code is simple

**Design Decision**: Decided to return boolean instead of count for clearer API

````

### Requirements

- Document 5 complete cycles
- Include code snippets at each phase
- Show test failures and successes
- Explain refactoring decisions
- Demonstrate design evolution

### Evaluation Criteria

| Criterion | Points | Description |
|-----------|--------|-------------|
| Completeness | 10 | All 5 cycles documented |
| Clarity | 8 | Clear explanations |
| Insight | 7 | Shows understanding of TDD |

---

## 🚀 Part 3: Advanced Features with TDD (20 points)

Implement 3 of the following features using TDD:

### Feature Options

1. **Late Fee Calculation**
   - $1 per day for overdue books
   - Due date is 14 days from borrow
   - Calculate total fees for a member

2. **Book Reservation System**
   - Reserve unavailable books
   - Queue system (FIFO)
   - Notify when book becomes available

3. **Search with Filters**
   - Search by genre, publication year, rating
   - Combined filters (AND logic)
   - Sort results

4. **Borrowing History**
   - Track all borrows and returns
   - Generate member history report
   - Calculate statistics (most borrowed book)

5. **Member Categories**
   - Student, Faculty, Public
   - Different borrow limits (3, 5, 2)
   - Different late fee rates

### Requirements

- Continue using TDD for all features
- Minimum 10 additional tests
- Git history shows RED-GREEN-REFACTOR

### Evaluation Criteria

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complexity | 8 | Features have meaningful logic |
| TDD Process | 7 | Continues test-first approach |
| Integration | 5 | Works with existing code |

---

## 📊 Part 4: Coverage & Quality (15 points)

### Requirements

1. **High Coverage**
   - Statement coverage >90%
   - Branch coverage >85%
   - Generate HTML coverage report

2. **Fast Tests**
   - Full test suite runs in <2 seconds
   - Use mocks for any slow operations
   - No skipped or ignored tests

3. **Test Quality**
   - Tests are independent
   - Clear, descriptive test names
   - One assertion per test (when reasonable)

### Generate Coverage

**Python**:
```bash
pytest --cov=. --cov-report=html --cov-report=term
open htmlcov/index.html
````

**JavaScript**:

```bash
npm test -- --coverage
open coverage/lcov-report/index.html
```

### Evaluation Criteria

| Criterion | Points | Description                     |
| --------- | ------ | ------------------------------- |
| Coverage  | 8      | >90% statement, >85% branch     |
| Speed     | 4      | Tests run in <2 seconds         |
| Quality   | 3      | Well-written, independent tests |

---

## 💭 Part 5: TDD Reflection (10 points)

Write a **500-700 word** reflection answering:

1. **Design Impact**: How did TDD influence your design decisions?
2. **Challenges**: What was difficult about test-first development?
3. **Benefits**: What advantages did you observe?
4. **Comparison**: How does TDD compare to test-after?
5. **Future Use**: When would/wouldn't you use TDD?
6. **Learning**: What surprised you? What would you do differently?

### Evaluation Criteria

| Criterion | Points | Description           |
| --------- | ------ | --------------------- |
| Depth     | 5      | Thoughtful analysis   |
| Insight   | 3      | Personal learning     |
| Writing   | 2      | Clear, well-organized |

---

## 🔄 Git Commit History Requirements

### CRITICAL: Your commit history MUST demonstrate TDD

Use this commit message format:

- **RED**: `RED: should calculate late fee for overdue books`
- **GREEN**: `GREEN: implement basic late fee calculation`
- **REFACTOR**: `REFACTOR: extract fee calculation to separate method`

### Example Commit History

```
RED: should create book with isbn, title, author
GREEN: implement Book class with basic properties
RED: should track available copies
GREEN: add available_copies property to Book
REFACTOR: rename copies parameter to total_copies for clarity
RED: should check if book is available
GREEN: implement is_available method
RED: should not be available when no copies
GREEN: handle zero copies in is_available
REFACTOR: simplify availability check logic
```

### Requirements

- Minimum 30 commits showing TDD cycles
- Each commit should be small (2-20 lines changed)
- Clear RED/GREEN/REFACTOR labels
- Logical progression of features

---

## 📤 Deliverables

Submit a GitHub repository containing:

### Required Files

```
library-management-system/
├── README.md (setup instructions, how to run tests)
├── requirements.txt or package.json
├── .gitignore
├── src/ or lib/
│   ├── book.py/js
│   ├── member.py/js
│   └── library.py/js
├── tests/
│   ├── test_book.py/js
│   ├── test_member.py/js
│   └── test_library.py/js
├── docs/
│   ├── tdd-process.md (Part 2: 5 cycles documented)
│   └── reflection.md (Part 5: reflection essay)
└── coverage/ (HTML coverage reports)
```

### Submission

1. Push all code to GitHub
2. Ensure commit history is clean and follows TDD format
3. Verify all tests pass on GitHub
4. Submit repository URL to Canvas

---

## 🎯 Grading Rubric

| Part                            | Points  | Criteria                                            |
| ------------------------------- | ------- | --------------------------------------------------- |
| **Part 1: Core Implementation** | 30      | Functionality (15), Coverage (8), TDD Adherence (7) |
| **Part 2: TDD Documentation**   | 25      | Completeness (10), Clarity (8), Insight (7)         |
| **Part 3: Advanced Features**   | 20      | Complexity (8), TDD Process (7), Integration (5)    |
| **Part 4: Coverage & Quality**  | 15      | Coverage (8), Speed (4), Quality (3)                |
| **Part 5: Reflection**          | 10      | Depth (5), Insight (3), Writing (2)                 |
| **Total**                       | **100** |                                                     |

### Bonus Opportunities (+10 points)

- **+5**: Implement in BOTH Python AND JavaScript using TDD
- **+3**: Create 5-10 minute video screencast showing live TDD session
- **+2**: Implement all 5 advanced features (not just 3)

---

## 💡 Tips for Success

1. **Start Simple**: Begin with the easiest test (e.g., object creation)
2. **Small Steps**: Write one test, make it pass, refactor, repeat
3. **Commit Often**: Commit after each GREEN and REFACTOR phase
4. **Watch Tests Fail**: Make sure test fails for the right reason (RED)
5. **Minimal Code**: In GREEN phase, write just enough to pass
6. **Refactor Fearlessly**: Tests give you confidence to improve code
7. **Read Test Names**: They should tell a story of your API
8. **Keep Tests Fast**: Mock external dependencies
9. **One Thing at a Time**: Don't test multiple behaviors in one test
10. **Enjoy the Rhythm**: RED-GREEN-REFACTOR becomes meditative with practice

---

## ⚠️ Common Mistakes to Avoid

❌ **Writing code before test** - Defeats TDD purpose  
❌ **Large commits** - Should be small, focused changes  
❌ **Vague commit messages** - Must clearly indicate RED/GREEN/REFACTOR  
❌ **Skipping refactor** - Tech debt accumulates  
❌ **Testing implementation details** - Test behavior, not internals  
❌ **Slow tests** - Mock dependencies to keep tests fast  
❌ **Interdependent tests** - Each test should run independently  
❌ **Writing multiple tests at once** - One test at a time!  
❌ **Not watching test fail first** - How do you know test is valid?  
❌ **Over-engineering in GREEN** - Just make it pass, refactor later

---

## ✅ Submission Checklist

Before submitting:

- [ ] All tests pass
- [ ] Coverage >90% statement, >85% branch
- [ ] Test suite runs in <2 seconds
- [ ] 30+ commits with RED/GREEN/REFACTOR labels
- [ ] Small, focused commits (not large batches)
- [ ] README with setup instructions
- [ ] TDD process documentation (5 cycles)
- [ ] Reflection essay (500-700 words)
- [ ] Coverage reports included
- [ ] Repository is public and accessible
- [ ] No commented-out code or tests
- [ ] Clean, readable code
- [ ] Meaningful test names

---

## 📚 Resources

- [Kent Beck: Test Driven Development](https://www.oreilly.com/library/view/test-driven-development/0321146530/)
- [Uncle Bob: Three Rules of TDD](http://butunclebob.com/ArticleS.UncleBob.TheThreeRulesOfTdd)
- [Martin Fowler: TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- [Review theory files](../theory/)
- [Practice with katas](../exercises/)

---

**Remember**: TDD is a discipline. It feels slow at first, but with practice you'll develop faster AND better! 🔄
