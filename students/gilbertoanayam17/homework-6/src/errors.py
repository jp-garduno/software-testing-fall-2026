"""Errors raised when an operation breaks one of the library's rules."""


class LibraryError(Exception):
    """Base class for every rule the library enforces."""


class BookNotAvailableError(LibraryError):
    """Raised when every copy of a book is already lent out."""


class InvalidReturnError(LibraryError):
    """Raised when something comes back that was never lent out."""


class BorrowLimitExceededError(LibraryError):
    """Raised when a member already holds as many books as their limit allows."""


class BookNotFoundError(LibraryError):
    """Raised when an ISBN is not in the catalog."""


class MemberNotFoundError(LibraryError):
    """Raised when a member id is not registered."""
