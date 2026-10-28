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


