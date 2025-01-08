from FileHandler import *
import csv
import pandas as pd

# def initialize_copies_available(books_df):
#     if "is_loaned" not in books_df.columns or "copies" not in books_df.columns:
#         raise ValueError("The DataFrame must contain 'is_loaned' and 'copies' columns.")
#
#     # Initialize the copies_available column
#     books_df["copies_available"] = books_df.apply(
#         lambda row: 0 if row["is_loaned"].strip().lower() == "yes" else row["copies"], axis=1
#     )
#     return books_df

def main():
    # # Load dataframes
    # books_df, available_books_df, loaned_books_df = FileHandler.read_csv_files()
    # # Initialize and save updated books_df
    # books_df = initialize_copies_available(books_df)
    # books_df.to_csv(Paths.BOOKS.value, index=False)  # Save changes back to CSV
    header = ["name", "password"]
    # Create the CSV file if it doesn't exist
    FileHandler.create_csv(Paths.USERS.value, header)
    FileHandler.init_loaned_books()
    FileHandler.init_available_books()


if __name__ == "__main__":
    main()
