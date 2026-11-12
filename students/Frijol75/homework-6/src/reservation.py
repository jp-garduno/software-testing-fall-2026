"""Reservation manager and record models."""
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Reservation:
    """Represents a reservation for an unavailable book."""

    reservation_id: str
    member_id: str
    isbn: str
    status: str = "PENDING"  # PENDING, NOTIFIED, FULFILLED, CANCELLED


class ReservationManager:
    """Maintains FIFO waitlists for unavailable books."""

    def __init__(self) -> None:
        self._queues: Dict[str, List[Reservation]] = {}
        self._latest_notified: Dict[str, str] = {}

    def add_reservation(self, reservation: Reservation) -> None:
        """Add a reservation to the book waitlist."""
        isbn = reservation.isbn
        if isbn not in self._queues:
            self._queues[isbn] = []
        self._queues[isbn].append(reservation)

    def get_queue(self, isbn: str) -> List[str]:
        """Return list of member IDs waiting for the book in FIFO order."""
        return [r.member_id for r in self._queues.get(isbn, []) if r.status == "PENDING"]

    def is_member_in_queue(self, member_id: str, isbn: str) -> bool:
        """Check if member already has a pending reservation for the book."""
        return member_id in self.get_queue(isbn)

    def cancel_reservation(self, member_id: str, isbn: str) -> bool:
        """Cancel a pending reservation."""
        queue = self._queues.get(isbn, [])
        for r in queue:
            if r.member_id == member_id and r.status == "PENDING":
                r.status = "CANCELLED"
                queue.remove(r)
                return True
        return False

    def notify_next(self, isbn: str) -> Optional[str]:
        """Notify next member in FIFO queue when a book is returned."""
        queue = self._queues.get(isbn, [])
        for r in queue:
            if r.status == "PENDING":
                r.status = "NOTIFIED"
                queue.remove(r)
                self._latest_notified[isbn] = r.member_id
                return r.member_id
        return None

    def get_latest_notified(self, isbn: str) -> Optional[str]:
        """Get the ID of the last member notified for a book."""
        return self._latest_notified.get(isbn)
