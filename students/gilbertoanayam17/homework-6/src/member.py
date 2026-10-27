"""Member: who can borrow, how many books at once, and which books they hold."""


class Member:
    """A registered library user."""

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []
