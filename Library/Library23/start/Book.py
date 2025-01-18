class Book:
    """
        A class to represent a book in the library system.
        Manages book details, availability, and waiting list.
    """
    def __init__(self, title, author, is_loaned, copies, genre, year):
        """
            Initializes a new Book instance.
            :param title: Title of the book.
            :param author: Author of the book.
            :param is_loaned: Indicates if the book is currently loaned ("Yes" or "No").
            :param copies: Total number of copies of the book.
            :param genre: Genre of the book.
            :param year: Publication year of the book.
        """
        self.title = title
        self.author = author
        self.is_loaned = is_loaned
        self.copies = copies
        self.genre = genre
        self.year = year
        self.request = 0
        self.loaned_count = 0

        # string to manage client names (FIFO)
        self.waiting_list = "empty"

        if is_loaned == "Yes":
            self.copies_available = 0
        else:
            self.copies_available = copies

    def update_details(self, title=None, author=None, is_loaned=None, copies=None, genre=None, year=None, request=None, loaned_count=None,waiting_list=None, copies_available=None):
        """
            Updates book attributes dynamically.
            Only updates the attributes provided in the arguments.
            :param kwargs: Dictionary of attributes to update.
        """
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
        if request:
            self.request = request
        if loaned_count:
            self.loaned_count = loaned_count
        if waiting_list:
            self.waiting_list = waiting_list
        if copies_available is not None:
            self.copies_available = copies_available

    def __str__(self):
        """
            Provides a readable string representation of the book's details.
            :return: String representation of the book.
        """
        return (f"Title: {self.title}, Author: {self.author}, Year: {self.year}, "
                f"Genre: {self.genre}, Copies: {self.copies}, "
                f"Loaned: {self.is_loaned}")
