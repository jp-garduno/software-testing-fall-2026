import pytest

from book import Book
from library import Library
from member import Member, MemberCategory

ISBN = "1234567890"


@pytest.fixture
def library(clock):
    lib = Library(clock=clock)
    lib.add_book(Book(ISBN, "Book One", "Author", copies=5))
    return lib


@pytest.mark.parametrize(
    "category, limit",
    [(MemberCategory.STUDENT, 3), (MemberCategory.FACULTY, 5), (MemberCategory.PUBLIC, 2)],
)
def test_borrow_limit_depends_on_category(category, limit):
    assert Member("m1", "Alice", category=category).max_borrow_limit == limit
