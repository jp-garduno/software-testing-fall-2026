# TDD cycle evidence for 5 cicles

## Cycle #1: IBM required min length

### RED Phase

**Test Written**:

```python
# # Test 4: IBM required length
def test_IBM_is_nine_digits():
    with pytest.raises(ValueError):
        book = Book("831957192", "Test Book")
```

**Test Result**: FAIL - book raises no error

### GREEN Phase

**Code Written**:

```python
if (len(ISBN) < 10):
			raise ValueError('Validation Error: ISBN must be 10 or 13 digits, title required')
```

**Test Result**: PASS - All tests green

### REFACTOR Phase

**Improvements Made**: Changed test name from (test_IBM_is_nine_digits) to (test_IBM_nine_digits_invalidated_correctly)

## Cycle #2: IBM required max length

### RED Phase

**Test Written**:

```python
# # Test 5: IBM required length
def test_IBM_fourteen_digits_invalidated_correctly():
    with pytest.raises(ValueError):
        book = Book("83195719123092", "Test Book")
```

**Test Result**: FAIL - book raises no error

### GREEN Phase

**Code Written**:

```python
if (len(ISBN) < 10 or len(ISBN) > 13):
```

**Test Result**: PASS - All tests green

### REFACTOR Phase

**Improvements Made**: No improvements needed

## Cycle #3: Borrow method

### RED Phase

**Test Written**:

```python
# # Test 5: IBM required length
def test_book_borrowed_four_times():
    book = Book("1234567890", "Test Book", "Author", copies=7)
    book.borrow()
    book.borrow()
    book.borrow()
    book.borrow()
    assert book.available_copies == 3
```

**Test Result**: FAIL - method borrow not implemented yet

### GREEN Phase

**Code Written**:

```python
def borrow(self):
	self.available_copies -= 1
```

**Test Result**: PASS - All tests green

### REFACTOR Phase

**Improvements Made**: No improvements needed

## Cycle #4: Return copy method

### RED Phase

**Test Written**:

```python
# # Test 5: IBM required length
def test_book_borrowed_and_returned_multiple_times():
    book = Book("1234567890", "Test Book", "Author", copies=23)
    book.borrow()
    book.borrow()
    book.return_book()
    book.borrow()
    book.return_book()
    assert book.available_copies == 22
```

**Test Result**: FAIL - method return_book not implemented yet

### GREEN Phase

**Code Written**:

```python
def returnBook(self):
	self.available_copies += 1
```

**Test Result**: PASS - All tests green

### REFACTOR Phase

**Improvements Made**: Changed returnBook method to return_book

## Cycle #5: Return copy method

### RED Phase

**Test Written**:

```python
# # Test 5: IBM required length
def test_book_returned_more_than_borrow_error():
    book = Book("1234567890", "Test Book", "Author", copies=23)
    book.borrow()
    book.borrow()
    book.return_book()
    book.borrow()
    book.return_book()
    book.return_book()
    with pytest.raises(ValueError):
        book.return_book()
```

**Test Result**: FAIL - method return book incorectly gives no error

### GREEN Phase

**Code Written**:

```python
def borrow(self):
	if (self.available_copies <= 0):
		raise ValueError('Invalid request: No copies left to borrow')
	self.available_copies -= 1

def return_book(self):
	if (self.available_copies == self.total_copies):
		raise ValueError('Invalid request: Cant return if no borrowed copies')
	self.available_copies += 
```

**Test Result**: PASS - All tests green

### REFACTOR Phase

**Improvements Made**: Changed returnBook method to return_book


