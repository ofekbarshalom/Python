from User import User
import Book

class Client(User):
    def __init__(self, name, password, is_librarian=False, borrowed_books=None):
        super().__init__(name, password, is_librarian)
        self.borrowed_books = borrowed_books if borrowed_books else []

    def lend_book(self, book):
        if book not in self.borrowed_books:
            self.borrowed_books.append(book)
            super().update_user_in_csv()
        else:
            print(f"Book '{book}' is already in {self.name}'s borrowed books.")

        super().update_user_in_csv()

    def return_book_to_library(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            super().update_user_in_csv()
        else:
            print(f"Book '{book}' is not in {self.name}'s borrowed books.")

        super().update_user_in_csv()
