"""Domain errors raised by the library system."""


class LibraryError(Exception):
    """Base class for every library rule violation."""


class BookUnavailableError(LibraryError):
    """Raised when no copy of a book is left to lend."""


class BorrowLimitExceededError(LibraryError):
    """Raised when a member already holds as many books as allowed."""
