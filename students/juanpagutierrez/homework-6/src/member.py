"""Library member who can borrow books."""


class Member:
    """A registered patron of the library."""

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
