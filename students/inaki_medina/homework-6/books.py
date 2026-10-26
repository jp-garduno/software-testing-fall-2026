class Book:
	def __init__(self, ISBN, title, author, copies = 1):
		self.ISBN = ISBN
		self.title = title
		self.author = author
		self.available_copies = copies

	def is_available(self): 
		return self.available_copies > 0


