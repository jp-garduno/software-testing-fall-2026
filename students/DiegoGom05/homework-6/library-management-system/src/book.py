class Book:
    def __init__(self, isbn, title, author, copies=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available_copies = copies
