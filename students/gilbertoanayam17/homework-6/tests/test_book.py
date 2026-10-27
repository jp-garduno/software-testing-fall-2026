"""Tests for Book: catalog data, copy tracking and validation."""

from src.book import Book


def test_should_store_isbn_title_and_author_when_created():
    book = Book("1234567890", "Clean Code", "Robert C. Martin")

    assert (book.isbn, book.title, book.author) == ("1234567890", "Clean Code", "Robert C. Martin")


def test_should_track_available_copies_when_created_with_copies():
    book = Book("1234567890", "Clean Code", "Robert C. Martin", copies=5)

    assert book.available_copies == 5


def test_should_be_available_when_copies_exist():
    book = Book("1234567890", "Clean Code", "Robert C. Martin", copies=1)

    assert book.is_available()
