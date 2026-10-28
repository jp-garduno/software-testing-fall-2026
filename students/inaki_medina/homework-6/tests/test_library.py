import library_system

Book = library_system.Book
Library = library_system.Library
Member = library_system.Member


def test_add_book_to_catalog():
    library = Library()
    book = Book("1234567890", "Test Book")

    library.add_book(book)

    assert book in library.books


def test_register_member():
    library = Library()
    member = Member("Juan")

    library.register_member(member)

    assert member in library.members


def test_borrow_book_updates_member_and_inventory():
    library = Library()
    book = Book("1234567890", "Test Book")
    member = Member("Juan")
    library.add_book(book)
    library.register_member(member)

    library.borrow_book(member.member_id, book.ISBN)

    assert book in member.borrowed_books
    assert book.available_copies == 0


def test_return_book_updates_member_and_inventory():
    library = Library()
    book = Book("1234567890", "Test Book")
    member = Member("Juan")
    book.borrow()
    member.add_borrowed_book(book)
    library.add_book(book)
    library.register_member(member)

    library.return_book(member.member_id, book.ISBN)

    assert book not in member.borrowed_books
    assert book.available_copies == 1


def test_search_by_title_returns_matching_books():
    library = Library()
    matching_book = Book("1234567890", "Test Book")
    other_book = Book("0987654321", "Other Book")
    library.add_book(matching_book)
    library.add_book(other_book)

    assert library.search_by_title("Test Book") == [matching_book]


def test_search_by_author_returns_matching_books():
    library = Library()
    matching_book = Book("1234567890", "Test Book", "Juan")
    other_book = Book("0987654321", "Other Book", "Maria")
    library.add_book(matching_book)
    library.add_book(other_book)

    assert library.search_by_author("Juan") == [matching_book]


def test_get_available_books_returns_only_available_books():
    library = Library()
    available_book = Book("1234567890", "Available Book")
    borrowed_book = Book("0987654321", "Borrowed Book")
    borrowed_book.borrow()
    library.add_book(available_book)
    library.add_book(borrowed_book)

    assert library.get_available_books() == [available_book]
