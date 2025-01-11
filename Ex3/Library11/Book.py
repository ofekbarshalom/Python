from queue import Queue

class Book:
    def __init__(self, title, author, is_loaned, copies, genre, year):
        self.title = title
        self.author = author
        self.is_loaned = is_loaned
        self.copies = copies
        self.genre = genre
        self.year = year
        self.request = 0
        self.loaned_count = 0

        # Queue to manage client names (FIFO)
        self.client_queue = Queue()

        if is_loaned:
            self.copies_available = 0
        else:
            self.copies_available = copies

    def return_book(self):
        if self.copies == self.copies_available:
            print("All books already returned")
        else:
            self.copies_available += 1

    def is_book_available(self):
        return self.copies_available > 0

    def update_details(self, title=None, author=None, is_loaned=None, copies=None, genre=None, year=None, copies_available=None):
        if title:
            self.title = title
        if author:
            self.author = author
        if is_loaned is not None:  # Explicitly check for None since is_loaned is a boolean
            self.is_loaned = is_loaned
        if copies is not None:  # Explicitly check for None in case copies is set to 0
            self.copies = copies
        if genre:
            self.genre = genre
        if year:
            self.year = year
        if copies_available is not None:
            self.copies_available = copies_available

    def get_title(self):
        return self.title

    def __str__(self):
        return (f"Title: {self.title}, Author: {self.author}, Year: {self.year}, "
                f"Genre: {self.genre}, Copies: {self.copies}, "
                f"Loaned: {self.is_loaned}")
