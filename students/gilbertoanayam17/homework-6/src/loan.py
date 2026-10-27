"""Loan: one copy lent to one member, when it is due and what lateness costs."""

from datetime import timedelta


class Loan:
    """A copy of a book lent to a member on a given date."""

    def __init__(self, member_id, isbn, borrowed_on):
        self.member_id = member_id
        self.isbn = isbn
        self.due_date = borrowed_on + timedelta(days=14)
