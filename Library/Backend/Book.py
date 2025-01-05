class Book:
    def __init__(self, title, author, is_loaned, copies, genre, year):
        self.title = title
        self.author = author
        self.is_loaned = is_loaned
        self.copies = copies
        self.genre = genre
        self.year = year

    def return_book(self):
        self.copies += 1

    def is_book_available(self):
        if self.copies > 0:
            self.copies -= 1
            return True
        return False

    def update_details(self, title=None, author=None, is_loaned=None, copies=None, genre=None, year=None):
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

    def get_title(self):
        return self.title

    def __str__(self):
        return (f"Title: {self.title}, Author: {self.author}, Year: {self.year}, "
                f"Genre: {self.genre}, Copies: {self.copies}, "
                f"Loaned: {self.is_loaned}")
