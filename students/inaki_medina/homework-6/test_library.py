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
