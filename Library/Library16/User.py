import hashlib
import csv
from path import Paths
from FileHandler import FileHandler
from Observer import Observer

class User(Observer):
    def __init__(self, name, password):
        self.name = name
        self.password = FileHandler.hash_password(password)
        self.messages = []

        # Automatically update the user in the CSV file
        self.add_user_in_csv()

    def add_user_in_csv(self, file_path=Paths.USERS.value):
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

    def update(self, message, users_df):
        self.messages.append(message)

        # Update the observer's messages in the users.csv file
        user_row_index = users_df[users_df["name"] == self.name].index
        if not user_row_index.empty:
            index = user_row_index[0]

            # Update the messages column
            if users_df.at[index, "messages"] == "empty":
                users_df.at[index, "messages"] = message
            else:
                users_df.at[index, "messages"] += f",{message}"
        else:
            print(f"Warning: Observer '{observer.name}' not found in users.csv.")
