"""Domain errors for the library management system."""


class LibraryError(Exception):
    """Base class for every error raised by the library domain."""


class InvalidBookError(LibraryError):
    """Raised when a book is created with invalid data."""


class NoCopiesAvailableError(LibraryError):
    """Raised when borrowing a book that has no available copies."""


class AllCopiesReturnedError(LibraryError):
    """Raised when returning a copy of a book whose copies are all on the shelf."""


class BorrowLimitReachedError(LibraryError):
    """Raised when a member tries to borrow beyond their limit."""


class BookNotBorrowedError(LibraryError):
    """Raised when returning a book the member does not have."""


class BookNotFoundError(LibraryError):
    """Raised when an ISBN is not in the catalog."""


class MemberNotFoundError(LibraryError):
    """Raised when a member ID is not registered."""


class DuplicateBookError(LibraryError):
    """Raised when adding a book whose ISBN is already in the catalog."""


class DuplicateMemberError(LibraryError):
    """Raised when registering a member ID twice."""


class AlreadyBorrowedError(LibraryError):
    """Raised when a member borrows a second copy of the same book."""


class ReservationError(LibraryError):
    """Raised when a reservation cannot be made or honored."""
