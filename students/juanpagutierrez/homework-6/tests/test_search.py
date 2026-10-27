"""Tests for search with filters and sorting (advanced feature 3)."""

import pytest

from src.book import Book
from src.library import Library


def test_book_stores_optional_genre_year_and_rating():
    book = Book("1234567890", "Clean Code", "Robert Martin", genre="Software", publication_year=2008, rating=4.4)
    assert (book.genre, book.publication_year, book.rating) == ("Software", 2008, 4.4)
