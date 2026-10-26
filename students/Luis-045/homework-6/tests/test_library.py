"""Integration tests for catalog and borrowing operations."""

import pytest

from src.book import Book
from src.library import Library
from src.member import Member


def test_library_starts_with_empty_catalog_and_members():
    library = Library()
    assert (library.catalog, library.members) == ({}, {})
