"""Tests for the Book class."""

from src.book import Book


def test_book_can_be_created_with_isbn_title_and_author():
    book = Book("1234567890", "Clean Code", "Robert Martin")
    assert (book.isbn, book.title, book.author) == ("1234567890", "Clean Code", "Robert Martin")
