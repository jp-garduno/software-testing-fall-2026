"""First come, first served reservations per book."""

from collections import defaultdict, deque


class ReservationQueue:
    """Keeps a FIFO queue of member ids for each ISBN."""

    def __init__(self):
        self._queues = defaultdict(deque)

    def add(self, isbn, member_id):
        self._queues[isbn].append(member_id)

    def pop_next(self, isbn):
        queue = self._queues[isbn]
        return queue.popleft() if queue else None

    def members_waiting(self, isbn):
        return list(self._queues[isbn])
