class Book:
    def __init__(self, isbn, title, author, copies=1):
        self.title = title
        self.isbn = isbn
        self.author = author
        self.available_copies = copies

    def is_available(self):
        return True
