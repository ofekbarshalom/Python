import hashlib
from path import Paths
from FileHandler import FileHandler
from Observer import Observer
import pandas as pd

class User(Observer):
    def __init__(self, name, password):
        self.name = name
        self.password = FileHandler.hash_password(password)
        self.messages = []

        # Automatically update the user in the CSV file
        self.add_user_in_csv()

    def add_user_in_csv(self):
        if FileHandler.check_name(self.name):
            print(f"User '{self.name}' already exists in files/users.csv.")
            return

        users_df = FileHandler.read_users_file()

        # Add new user to the DataFrame
        new_user = pd.DataFrame({"name": [self.name], "password": [self.password], "messages": ["empty"]})
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_csv(Paths.USERS.value, index=False)

    @staticmethod
    def add_book_to_library(book):
        books_df, available_books_df,_ = FileHandler.read_csv_files()

        # Add the new book
        new_book = pd.DataFrame([{
            "title": book.title,
            "author": book.author,
            "is_loaned": book.is_loaned,
            "copies": book.copies,
            "genre": book.genre,
            "year": book.year,
            "copies_available": book.copies_available,
            "waiting_list": book.waiting_list,
            "loaned_count": book.loaned_count
        }])
        books_df = pd.concat([books_df, new_book], ignore_index=True)
        books_df.to_csv(file_path, index=False)

        new_available_book = pd.DataFrame([{
            "title": book.title,
            "copies_available": book.copies_available
        }])
        available_books_df = pd.concat([available_books_df, new_available_book], ignore_index=True)
        available_books_df.to_csv(available_books_path, index=False)

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
            print(f"Warning: Observer '{Observer.name}' not found in users.csv.")
