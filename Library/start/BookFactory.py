from start.Book import Book
class BookFactory:
    """
        Factory class for creating Book objects with validation and default values.
    """
    @staticmethod
    def create_book(title, author, is_loaned=False, copies=1, genre="Unknown", year=None):
        """
            Creates a Book object with the specified attributes.
            :param title: Title of the book (required).
            :param author: Author of the book (required).
            :param is_loaned: Loan status of the book (default: False).
            :param copies: Total number of copies (default: 1).
            :param genre: Genre of the book (default: "Unknown").
            :param year: Publication year (default: None).
            :return: An instance of the Book class.
            :raises ValueError: If required fields are missing or invalid values are provided.
        """
        # Validation for book creation
        if not title or not author:
            raise ValueError("Title and author are required to create a book.")

        if int(copies) < 0:
            raise ValueError("Number of copies cannot be negative.")

        return Book(title, author, is_loaned, copies, genre, year)
