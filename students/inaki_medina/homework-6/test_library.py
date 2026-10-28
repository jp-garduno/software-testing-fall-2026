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
