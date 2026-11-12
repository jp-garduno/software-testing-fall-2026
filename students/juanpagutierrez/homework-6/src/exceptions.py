"""Domain errors raised by the library system."""


class LibraryError(Exception):
    """Base class for every library rule violation."""


class BookUnavailableError(LibraryError):
    """Raised when no copy of a book is left to lend."""


class BorrowLimitExceededError(LibraryError):
    """Raised when a member already holds as many books as allowed."""


class BookNotFoundError(LibraryError):
    """Raised when an ISBN is not in the catalog."""


class MemberNotFoundError(LibraryError):
    """Raised when a member id is not registered."""


class ReservationError(LibraryError):
    """Raised when a reservation request breaks a reservation rule."""
