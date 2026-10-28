from book import Book
from library import Library
from member import Member


def test_library_adds_books_and_registers_members():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert Martin")
    member = Member("m-1", "Ada")

    library.add_book(book)
    library.register_member(member)

    assert library.books[book.isbn] is book
