import books

Book = books.Book

# Test 1: Book exists
def test_book_can_be_created():
    book = Book("1234567890", "Test Book", "Author")
    assert book.title == "Test Book"

# # Test 2: Book has copies
# def test_book_has_available_copies():
#     book = Book("1234567890", "Test Book", "Author", copies=5)
#     assert book.available_copies == 5

# # Test 3: Can check availability
# def test_book_is_available_when_copies_exist():
#     book = Book("1234567890", "Test Book", "Author", copies=1)
#     assert book.is_available() == True

# Continue with more tests...