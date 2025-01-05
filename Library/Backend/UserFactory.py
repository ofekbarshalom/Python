from User import User  # Import the User class from user.py
from Librarian import Librarian
from Client import Client  # Import the Librarian class from librarian.py


class UserFactory:
    @staticmethod
    def create_user(name, password, is_librarian=False, borrowed_books=None):
        # Validation for user creation
        if not name or not password:
            raise ValueError("Name and Password are required to create a user.")

        if is_librarian:
            return Librarian(name, password)
        else:
            return Client(name, password, is_librarian, borrowed_books)
