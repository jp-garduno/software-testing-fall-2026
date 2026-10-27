"""Errors raised when an operation breaks one of the library's rules."""


class LibraryError(Exception):
    """Base class for every rule the library enforces."""


class BookNotAvailableError(LibraryError):
    """Raised when every copy of a book is already lent out."""
