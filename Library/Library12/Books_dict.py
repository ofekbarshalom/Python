from FileHandler import FileHandler
from Book import Book
from queue import Queue
from path import Paths
import pandas as pd


books_dict = {}

def initialize_books_dict():
    global books_dict
    books_dict = FileHandler.create_books_dict_from_csv()  # Initialize using FileHandler
    print("Global books_dict has been initialized.")

def add_book_to_dict(book):
    if book.title in books_dict:
        print(f"Book '{book.title}' already exists in the dictionary.")
        return
    books_dict[book.title] = book
    print(f"Book '{book.title}' added to the dictionary.")

def remove_book_from_dict(book_title):
    if book_title in books_dict:
        del books_dict[book_title]
        print(f"Book '{book_title}' removed from the dictionary.")
        return
    print(f"Book '{book_title}' not found in the dictionary.")

def get_book_object(book_title):
    if book_title in books_dict:
        return books_dict[book_title]
    else:
        print(f"Book '{book_title}' not found in the dictionary.")
        return None

def update_book_waiting_list(book_title, client_name):
    if book_title in books_dict:
        # Retrieve the book object
        book = books_dict[book_title]

        # Add the client to the book's queue
        book.client_queue.put(client_name)
        book.request += 1
        check_and_update_book_in_popular_books(book_title, book.request)

        # Print confirmation message
        print(f"Client '{client_name}' added to the waiting list of book '{book_title}'.")
        return True

    # Book not found in the dictionary
    print(f"Book '{book_title}' not found in the dictionary.")
    return False

def check_and_update_book_in_popular_books(book_title, book_request_and_loaned_count):
    # Load the popular_books.csv file into a DataFrame
    popular_books_df = FileHandler.read_popular_books_file()

    row_count = popular_books_df.shape[0]
    if row_count >= 10:
        lowest_count_book_title, lowest_count_book_total = get_book_with_lowest_requests_and_loans(popular_books_df)

        if lowest_count_book_total < book_request_and_loaned_count:
            update_book_in_popular_books(book_title, popular_books_df, book_request_and_loaned_count)
    else:
        update_book_in_popular_books(book_title, popular_books_df, book_request_and_loaned_count)


def update_book_in_popular_books(book_title, popular_books_df, book_request_and_loaned_count):
    # Check if the book exists in the DataFrame
    if book_title in popular_books_df["title"].values:
        # Update or remove the book based on the book_request value
        if book_request_and_loaned_count == 0:
            # Remove the book
            popular_books_df = popular_books_df[popular_books_df["title"] != book_title]
            print(f"Book '{book_title}' removed from popular_books.csv as request count is 0.")
        else:
            # Update the book_request value
            popular_books_df.loc[
                popular_books_df["title"] == book_title, "requests"] = book_request_and_loaned_count
            print(f"Book '{book_title}' updated with request count {book_request_and_loaned_count}.")
    else:
        # Add the book if it doesn't exist
        if book_request_and_loaned_count > 0:
            new_row = {"title": book_title, "requests": book_request_and_loaned_count}
            popular_books_df = pd.concat([popular_books_df, pd.DataFrame([new_row])], ignore_index=True)
            print(
                f"Book '{book_title}' added to popular_books.csv with request count {book_request_and_loaned_count}.")
        else:
            print(f"Book '{book_title}' not added as request count is 0.")

    # Save the updated DataFrame back to the CSV file
    popular_books_df.to_csv(Paths.POPULAR_BOOKS.value, index=False)

def get_book_with_lowest_requests_and_loans(popular_books_df):
    if popular_books_df.empty:
        print("The popular_books DataFrame is empty.")
        return None

    # Find the row with the minimum requests value
    min_row = popular_books_df.loc[popular_books_df["requests"].idxmin()]

    # Return the book title and the requests count
    return min_row["title"], min_row["requests"]
