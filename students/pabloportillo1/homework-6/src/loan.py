from datetime import timedelta

LOAN_PERIOD = timedelta(days=14)


class Loan:
    def __init__(self, member_id, isbn, borrowed_on):
        self.member_id = member_id
        self.isbn = isbn
        self.borrowed_on = borrowed_on
        self.due_on = borrowed_on + LOAN_PERIOD
        self.returned_on = None

    def days_overdue(self, today):
        return max(0, ((self.returned_on or today) - self.due_on).days)
