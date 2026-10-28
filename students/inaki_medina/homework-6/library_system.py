import uuid

class Book:
	def __init__(self, ISBN, title, author = "", copies = 1):
		if (len(ISBN) < 10 or len(ISBN) > 13):
			raise ValueError('Validation Error: ISBN must be 10 or 13 digits, title required')
		self.ISBN = ISBN
		self.title = title
		self.author = author
		self.total_copies = copies
		self.available_copies = copies

	def is_available(self): 
		return self.available_copies > 0

	def borrow(self):
		if (self.available_copies <= 0):
			raise ValueError('Invalid request: No copies left to borrow')
		self.available_copies -= 1

	def return_book(self):
		if (self.available_copies == self.total_copies):
			raise ValueError('Invalid request: Cant return if no borrowed copies')
		self.available_copies += 1


class Member:
	def __init__(self, name, borrowed_books=None, max_borrow_limit=3):
		self.member_id = uuid.uuid4()
		self.name = name
		self.borrowed_books = list(borrowed_books) if borrowed_books is not None else []
		self.max_borrow_limit = max_borrow_limit

	def can_borrow(self):
		return len(self.borrowed_books) < self.max_borrow_limit

	def add_borrowed_book(self, book):
		if not self.can_borrow():
			raise ValueError("Invalid request: Member has reached the borrowing limit")
		self.borrowed_books.append(book)

	def return_book(self, book):
		self.borrowed_books.remove(book)


class Library:
	def __init__(self):
		self.books = []
		self.members = []

	def add_book(self, book):
		self.books.append(book)

	def register_member(self, member):
		self.members.append(member)

	def borrow_book(self, member_id, isbn):
		member = next((member for member in self.members if member.member_id == member_id), None)
		if member is None:
			raise ValueError("Invalid request: Member is not registered")

		book = next((book for book in self.books if book.ISBN == isbn), None)
		if book is None:
			raise ValueError("Invalid request: Book is not in the catalog")

		if not member.can_borrow():
			raise ValueError("Invalid request: Member has reached the borrowing limit")

		book.borrow()
		member.add_borrowed_book(book)

	def return_book(self, member_id, isbn):
		member = next((member for member in self.members if member.member_id == member_id), None)
		if member is None:
			raise ValueError("Invalid request: Member is not registered")

		book = next((book for book in self.books if book.ISBN == isbn), None)
		if book is None:
			raise ValueError("Invalid request: Book is not in the catalog")

		if book not in member.borrowed_books:
			raise ValueError("Invalid request: Member has not borrowed this book")

		book.return_book()
		member.return_book(book)

	def search_by_title(self, title):
		return [book for book in self.books if title.lower() in book.title.lower()]

	def search_by_author(self, author):
		return [book for book in self.books if author.lower() in book.author.lower()]

	def get_available_books(self):
		return [book for book in self.books if book.is_available()]
