import csv
import hashlib
from Book import Book  # Import the Book class


class User:

    def __init__(self, name, password, is_librarian=False):
        self.name = name
        self.password = self.hash_password(password)
        self.is_admin = is_librarian
        self.borrowed_books = []  # Initialize borrowed_books

        # Automatically update the user in the CSV file
        self.add_user_in_csv()

    @staticmethod
    def hash_password(password):
        # Create an SHA-256 hash object
        hash_object = hashlib.sha256()

        # Encode the password to bytes, then hash it
        hash_object.update(password.encode('utf-8'))

        # Get the hexadecimal representation of the hash
        return hash_object.hexdigest()

    @staticmethod
    def create_csv(file_path="users.csv"):
        # Write user details to a CSV file
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(["name", "password", "is_admin", "borrowed_books"])

    def add_user_in_csv(self, file_path="users.csv"):
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write a row with user details
            writer.writerow([self.name, self.password, self.is_admin, self.get_borrowed_books_titles()])

    def get_borrowed_books_titles(self):
        names = []
        for book in self.borrowed_books:
            names.append(book.get_title())

        return ", ".join(names)

    def update_user_in_csv(self, file_path="users.csv"):
        rows = []

        try:
            # Read the existing file
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            # Update user details
            user_found = False
            for row in rows:
                if row["name"] == self.name:  # Find the user by name
                    row["password"] = self.password
                    row["is_admin"] = self.is_admin
                    row["borrowed_books"] = self.get_borrowed_books_titles()
                    user_found = True
                    break

            if not user_found:
                raise ValueError(f"User with name '{self.name}' not found in the CSV file.")

            # Write updated rows back to the file
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["name", "password", "is_admin", "borrowed_books"])
                writer.writeheader()
                writer.writerows(rows)

        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    @staticmethod
    def check_login(name, password, file_path="users.csv"):
        try:
            # Open the CSV file for reading
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Check each row for the username
                for row in reader:
                    if row["name"] == name:  # Username found
                        hashed_password = self.hash_password(password)
                        if row["password"] == hashed_password:  # Check if passwords match
                            return True  # Username and password are correct
                        else:
                            print("Password is incorrect")
                            return False  # Incorrect password

                print("Username is incorrect")
                return False  # Username not found

        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        except Exception as e:
            raise Exception(f"An error occurred while checking the username: {e}")


