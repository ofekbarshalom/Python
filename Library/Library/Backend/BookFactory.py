class BookFactory:
    @staticmethod
    def create_book(name, password, is_loaned=False, copies=1, genre="Unknown", year=None):
        # Validation for book creation
        if not title or not author:
            raise ValueError("Title and author are required to create a book.")

        if copies < 0:
            raise ValueError("Number of copies cannot be negative.")

        return Book(title, author, is_loaned, copies, genre, year)
