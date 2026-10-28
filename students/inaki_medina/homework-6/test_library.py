import library_system

Book = library_system.Book
Library = library_system.Library


def test_add_book_to_catalog():
    library = Library()
    book = Book("1234567890", "Test Book")

    library.add_book(book)

    assert book in library.books
