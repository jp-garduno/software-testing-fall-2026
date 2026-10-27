"""Tests for search with filters and sorting (advanced feature 3)."""

import pytest

from src.book import Book
from src.library import Library


def test_book_stores_optional_genre_year_and_rating():
    book = Book("1234567890", "Clean Code", "Robert Martin", genre="Software", publication_year=2008, rating=4.4)
    assert (book.genre, book.publication_year, book.rating) == ("Software", 2008, 4.4)


@pytest.mark.parametrize("rating", [-0.1, 5.1])
def test_rating_outside_zero_to_five_is_rejected(rating):
    with pytest.raises(ValueError):
        Book("1234567890", "Clean Code", "Robert Martin", rating=rating)


@pytest.fixture(name="library")
def library_fixture():
    """A catalog with books of different genres, years and ratings."""
    library = Library()
    library.add_book(Book("1111111111", "Clean Code", "Robert Martin",
                          genre="Software", publication_year=2008, rating=4.4))
    library.add_book(Book("2222222222", "Dune", "Frank Herbert",
                          genre="Science Fiction", publication_year=1965, rating=4.3))
    library.add_book(Book("3333333333", "Refactoring", "Martin Fowler",
                          genre="Software", publication_year=2018, rating=4.2))
    library.add_book(Book("4444444444", "Neuromancer", "William Gibson",
                          genre="Science Fiction", publication_year=1984, rating=3.9))
    return library


def isbns(books):
    """ISBNs of ``books``, in order, for compact assertions."""
    return [book.isbn for book in books]


def test_search_filters_by_genre(library):
    assert isbns(library.search(genre="Software")) == ["1111111111", "3333333333"]


def test_search_filters_by_publication_year(library):
    assert isbns(library.search(publication_year=1965)) == ["2222222222"]


def test_search_filters_by_minimum_rating(library):
    assert isbns(library.search(min_rating=4.3)) == ["1111111111", "2222222222"]


def test_search_combines_filters_with_and_logic(library):
    assert isbns(library.search(genre="Science Fiction", min_rating=4.0)) == ["2222222222"]


def test_search_results_can_be_sorted_by_a_field(library):
    assert isbns(library.search(genre="Science Fiction", sort_by="publication_year")) == ["2222222222", "4444444444"]
