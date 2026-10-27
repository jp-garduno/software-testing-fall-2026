"""Tests for Book: catalog data, copy tracking and validation."""

from src.book import Book


def test_should_store_isbn_title_and_author_when_created():
    book = Book("1234567890", "Clean Code", "Robert C. Martin")

    assert (book.isbn, book.title, book.author) == ("1234567890", "Clean Code", "Robert C. Martin")
