"""Reservation queues and holds for books that are out on loan."""

from collections import deque

from src.exceptions import ReservationError


class ReservationDesk:
    """FIFO waiting lists per ISBN, and copies held for notified members."""

    def __init__(self, notifier=None):
        self._notifier = notifier
        self._queues = {}
        self._holds = {}

    def reserve(self, member_id, isbn):
        """Add ``member_id`` to the end of the waiting list for ``isbn``."""
        queue = self._queues.setdefault(isbn, deque())
        if member_id in queue:
            raise ReservationError(f"{member_id} already reserved {isbn}")
        queue.append(member_id)

    def queue(self, isbn):
        """Member ids waiting for ``isbn``, first in line first."""
        return list(self._queues.get(isbn, ()))

    def copy_returned(self, isbn):
        """Hold the returned copy for the next member in line and notify them."""
        queue = self._queues.get(isbn)
        if not queue:
            return
        next_member = queue.popleft()
        self._holds.setdefault(isbn, []).append(next_member)
        if self._notifier is not None:
            self._notifier.notify(next_member, isbn)

    def blocks(self, member_id, isbn, available_copies):
        """True when every free copy of ``isbn`` is held for someone other than ``member_id``."""
        holds = self._holds.get(isbn, [])
        return bool(holds) and member_id not in holds and available_copies <= len(holds)

    def release(self, member_id, isbn):
        """Drop the hold ``member_id`` had on ``isbn``, if any."""
        holds = self._holds.get(isbn, [])
        if member_id in holds:
            holds.remove(member_id)
