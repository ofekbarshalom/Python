import hashlib
import csv
from path import Paths
from Observer import Observer
from utils import utils

class User(Observer):
    def __init__(self, name, password):
        self.name = name
        self.password = utils.hash_password(password)
        self.messages = []

        # Automatically update the user in the CSV file
        self.add_user_in_csv()

    def add_user_in_csv(self, file_path=Paths.USERS.value):
        from FileHandler import FileHandler
        if not FileHandler.check_name(self.name):
            with open(file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Write a row with user details
                writer.writerow([self.name, self.password])

    @staticmethod
    def add_book_to_library(book, file_path=Paths.BOOKS.value):
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write a row with book details
            writer.writerow([book.title, book.author, book.is_loaned, book.copies, book.genre, book.year, book.copies_available])

        with open(Paths.AVAILABLE_BOOKS.value, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write a row with book details
            writer.writerow([book.title, book.copies_available])

    # @staticmethod
    # def remove_book_from_library(book_title):
    #     FileHandler.remove_book_from_csv(book_title, Paths.BOOKS.value)
    #     FileHandler.remove_book_from_csv(book_title, Paths.AVAILABLE_BOOKS.value)
    #     FileHandler.remove_book_from_csv(book_title, Paths.LOANED_BOOKS.value)

    def update(self, message):
        self.messages.append(message)
        print(f"User {self.name} received message: {message}")

    def clear_messages(self):
        self.messages.clear()



