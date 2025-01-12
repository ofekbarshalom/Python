from FileHandler import *
import csv
import pandas as pd

def initialize_copies_available(books_df):
    if "is_loaned" not in books_df.columns or "copies" not in books_df.columns:
        raise ValueError("The DataFrame must contain 'is_loaned' and 'copies' columns.")

    # Check if 'copies_available' column already exists
    if "copies_available" not in books_df.columns:
        # Initialize the copies_available column
        books_df["copies_available"] = books_df.apply(
            lambda row: 0 if row["is_loaned"].strip().lower() == "yes" else row["copies"], axis=1
        )
        print("Initialized 'copies_available' column.")
    else:
        print("'copies_available' column already exists. Skipping initialization.")

    return books_df


def initialize_waiting_list(books_df):
    # Check if 'waiting_list' column already exists
    if "waiting_list" not in books_df.columns:
        # Add a new 'waiting_list' column, initialized with empty Queue objects
        books_df["waiting_list"] = ""
        print("Initialized 'waiting_list' column with empty strings.")
    else:
        print("'waiting_list' column already exists. Skipping initialization.")

    return books_df

def initialize_loaned_count(books_df):
    # Check if 'loaned_count' column already exists
    if "loaned_count" not in books_df.columns:
        # Add a new 'loaned_count' column, initialized to 0
        books_df["loaned_count"] = 0
        print("Initialized 'loaned_count' column with all values set to 0.")
    else:
        print("'loaned_count' column already exists. Skipping initialization.")

    return books_df
def main():
    # Load dataframes
    books_df, available_books_df, loaned_books_df = FileHandler.read_csv_files()
    # Initialize and save updated books_df
    books_df = initialize_copies_available(books_df)
    books_df = initialize_waiting_list(books_df)
    books_df = initialize_loaned_count(books_df)

    books_df.to_csv(Paths.BOOKS.value, index=False)  # Save changes back to CSV
    users_file_header = ["name", "password"]
    # Create the CSV file if it doesn't exist
    FileHandler.create_csv(Paths.USERS.value, users_file_header)

    popular_books_file_header = ["title", "requests"]
    # Create the CSV file if it doesn't exist
    FileHandler.create_csv(Paths.POPULAR_BOOKS.value, popular_books_file_header)

    FileHandler.init_loaned_books()
    FileHandler.init_available_books()
    FileHandler.init_logs()


if __name__ == "__main__":
    main()
