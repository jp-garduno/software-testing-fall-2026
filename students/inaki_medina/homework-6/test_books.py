import books
import pytest

Book = books.Book

# Test 1: Book exists
def test_book_can_be_created():
    book = Book("1234567890", "Test Book", "Author")
    assert book.title == "Test Book"

# # Test 2: Book has copies
def test_book_has_available_copies():
    book = Book("1234567890", "Test Book", "Author", copies=5)
    assert book.available_copies == 5

# # Test 3: Can check availability
def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Test Book", "Author", copies=1)
    assert book.is_available() == True

# # Test 4: IBM required length
def test_IBM_nine_digits_invalidated_correctly():
    with pytest.raises(ValueError):
        book = Book("831957192", "Test Book")

# # Test 4: IBM required length
def test_IBM_fourteen_digits_invalidated_correctly():
    with pytest.raises(ValueError):
        book = Book("83195719123092", "Test Book")

# # Test 5: Borrow method
def test_book_borrowed_four_times():
    book = Book("1234567890", "Test Book", "Author", copies=7)
    book.borrow()
    book.borrow()
    book.borrow()
    book.borrow()
    assert book.available_copies == 3

# # Test 6: Return copy method
def test_book_borrowed_and_returned_multiple_times():
    book = Book("1234567890", "Test Book", "Author", copies=23)
    book.borrow()
    book.borrow()
    book.return_book()
    book.borrow()
    book.return_book()
    assert book.available_copies == 22

# # Test 7: Return excess
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

# # Test 8: borrow try with no copies
def test_borrow_with_zero_copies():
    book = Book("1234567890", "Test Book", "Author", copies=3)
    book.borrow()
    book.borrow()
    book.borrow()
    with pytest.raises(ValueError):
        book.borrow()


