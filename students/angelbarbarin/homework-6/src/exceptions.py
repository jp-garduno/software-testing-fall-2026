"""Domain exceptions for the library management system."""


class LibraryError(Exception):
    """Base class for every library rule violation."""


class BookNotAvailableError(LibraryError):
    """Raised when no copies of a book are available."""


class InvalidReturnError(LibraryError):
    """Raised when returning a copy that was never lent."""


class BorrowLimitExceededError(LibraryError):
    """Raised when a member already has the maximum number of books."""


class MemberNotFoundError(LibraryError):
    """Raised when a member id is not registered."""


class BookNotFoundError(LibraryError):
    """Raised when an ISBN is not part of the catalog."""


class AlreadyBorrowedError(LibraryError):
    """Raised when a member tries to borrow a book they already have."""


class ReservationError(LibraryError):
    """Raised when a reservation does not make sense."""
