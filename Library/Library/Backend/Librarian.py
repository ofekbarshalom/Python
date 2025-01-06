from Book import Book  # Import the Book class
import hashlib
import csv

class Librarian:
    def __init__(self, name, password):
        self.name = name
        self.password = self.hash_password(password)

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

    def add_user_in_csv(self, file_path="users.csv"):
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write a row with user details
            writer.writerow([self.name, self.password])

    @staticmethod
    def check_login(name, password, file_path="users.csv"):
        try:
            # Open the CSV file for reading
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Check each row for the username
                for row in reader:
                    if row["name"] == name:  # Username found
                        hashed_password = Librarian.hash_password(password)
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

    @staticmethod
    def add_book_to_library(book, file_path="books.csv"):
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write a row with book details
            writer.writerow([book.title, book.author, book.is_loaned, book.copies, book.genre, book.year])
