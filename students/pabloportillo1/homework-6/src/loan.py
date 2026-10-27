from datetime import timedelta

LOAN_PERIOD = timedelta(days=14)


class Loan:
    def __init__(self, member_id, isbn, borrowed_on):
        self.member_id = member_id
        self.isbn = isbn
        self.borrowed_on = borrowed_on
        self.due_on = borrowed_on + LOAN_PERIOD
