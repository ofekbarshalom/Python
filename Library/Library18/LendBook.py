import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from FileHandler import FileHandler
from utils import utils
from path import Paths
from logger import Logger

# Get the logger instance
log = Logger.get_logger()

def update_loaned_count(book_title, books_df):
    # Check if the book exists in books_df
    if book_title not in books_df["title"].values:
        print(f"Book '{book_title}' not found in the DataFrame.")
        return False

    # Increment the loaned_count for the specific book
    book_row_index = books_df.index[books_df["title"] == book_title][0]
    books_df.at[book_row_index, "loaned_count"] += 1

    # Save the updated DataFrame to the CSV
    books_df.to_csv(Paths.BOOKS.value, index=False)

    # Retrieve the updated loaned_count
    loaned_count = books_df.at[book_row_index, "loaned_count"]

    # Retrieve the waiting_list string
    waiting_list_str = books_df.at[book_row_index, "waiting_list"]

    # Calculate the number of requests (names in the waiting list)
    if waiting_list_str != "empty":
        request_count = len(waiting_list_str.split(","))
    else:
        request_count = 0

    # Calculate the total for popular books logic
    book_request_and_loaned_count = request_count + loaned_count

    utils.check_and_update_book_in_popular_books(book_title, book_request_and_loaned_count)
    print(f"'loaned_count' for '{book_title}' incremented by 1.")
    return True


def add_book_to_loaned_books(book_title, loaned_books_df):
    # Add the book to loaned_books.csv
    loaned_books_entry = pd.DataFrame({"title": [book_title]})
    loaned_books_df = pd.concat([loaned_books_df, loaned_books_entry], ignore_index=True)
    loaned_books_df.to_csv(Paths.LOANED_BOOKS.value, index=False)
    # Print success message
    print(f"'{book_title}' has been loaned out. All copies are now loaned!")


def remove_book_from_available_books(book_title, available_books_df):
    # Remove the book from available_books.csv
    available_books_df = available_books_df[available_books_df["title"] != book_title]

    # Save the updated available_books.csv
    available_books_df.to_csv(Paths.AVAILABLE_BOOKS.value, index=False)

    print(f"'{book_title}' has been removed from available_books.csv.")


def change_is_loaned(book_title,books_df):
    # Update the is_loaned status to "Yes"
    books_df.loc[books_df["title"] == book_title, "is_loaned"] = "Yes"

    # Save the updated DataFrame back to the CSV file
    books_df.to_csv(Paths.BOOKS.value, index=False)

    print(f"'is_loaned' status for '{book_title}' has been updated to 'Yes'.")

    return books_df


def decrement_copies_available_in_available_books(book_title, available_books_df, copies_available):
    # Decrement copies_available for the book in available_books.csv
    available_books_df.loc[available_books_df["title"] == book_title, "copies_available"] -= 1

    # Save the updated available_books.csv
    available_books_df.to_csv(Paths.AVAILABLE_BOOKS.value, index=False)
    print(f"'{book_title}' now has {copies_available - 1} copies available in available_books.csv.")


def decrement_copies_available_in_books(book_title, books_df, copies_available):
    # Decrement copies_available in books.csv
    books_df.loc[books_df["title"] == book_title, "copies_available"] -= 1

    # Save the updated books.csv
    books_df.to_csv(Paths.BOOKS.value, index=False)
    print(f"'{book_title}' now has {copies_available - 1} copies available in books.csv.")


def check_book_request(book_title, books_df):
    # Check if the book exists in books_df
    if book_title not in books_df["title"].values:
        print(f"Book '{book_title}' not found in the DataFrame.")
        return None

    # Get the row index for the specific book
    book_row_index = books_df.index[books_df["title"] == book_title][0]

    # Retrieve the waiting_list string
    waiting_list_str = books_df.at[book_row_index, "waiting_list"]

    # Check if the waiting list string is not empty
    if waiting_list_str != "empty":
        # Convert the waiting list string to a list of names
        waiting_list = waiting_list_str.split(",")

        # Return the first name in the waiting list
        first_request = waiting_list[0]
        return first_request

    # If the waiting list string is empty, return None
    print(f"The waiting list for '{book_title}' is empty.")
    return None


def remove_first_request(book_title, books_df):
    # Check if the book exists in books_df
    if book_title not in books_df["title"].values:
        print(f"Book '{book_title}' not found in the DataFrame.")
        return False

    # Get the row index for the specific book
    book_row_index = books_df.index[books_df["title"] == book_title][0]

    # Retrieve the waiting_list string
    waiting_list_str = books_df.at[book_row_index, "waiting_list"]

    # Check if the waiting list is not empty
    if waiting_list_str != "empty":
        # Convert the string to a list of names
        waiting_list = waiting_list_str.split(",")

        # Remove the first request
        removed_request = waiting_list.pop(0)

        # Update the waiting_list column
        updated_waiting_list_str = ",".join(waiting_list)
        books_df.at[book_row_index, "waiting_list"] = updated_waiting_list_str

        # Save the updated DataFrame back to the CSV file
        books_df.to_csv(Paths.BOOKS.value, index=False)

        # Print debug information
        print(f"Removed request: '{removed_request}' from the waiting list of '{book_title}'.")
        return True

    # If the waiting list is empty
    print(f"The waiting list for '{book_title}' is already empty.")
    return False

def check_waiting_list_name(book_title, alert_label, books_df):
    first_in_queue = check_book_request(book_title, books_df)

    if first_in_queue:
        text = f"'{book_title}' has a waiting list.\nIf you're first, the book will be loaned to you."
        client_name = utils.get_name_popup(text)

        if client_name == first_in_queue:
            remove_first_request(book_title, books_df)
            return True
        else:
            alert_label.config(text=f"'{client_name}' not the first at the waiting list", fg="red")
            alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
            return False
    else:
        return True


def update_files(book_title):
    books_df, available_books_df, loaned_books_df = FileHandler.read_csv_files()

    # Find the book in books_df and get the copies_available
    try:
        copies_available = int(books_df.loc[books_df["title"] == book_title, "copies_available"].values[0])
    except IndexError:
        print(f"Book '{book_title}' not found in the main books.csv!")
        return

    # Check if copies_available 1
    if copies_available == 1:
        add_book_to_loaned_books(book_title, loaned_books_df)
        remove_book_from_available_books(book_title, available_books_df)
        books_df = change_is_loaned(book_title, books_df)
    else:
        decrement_copies_available_in_available_books(book_title, available_books_df, copies_available)

    # Print remaining copies and decrement copies_available in files
    print(f"'{book_title}' has {copies_available - 1} copies available.")
    decrement_copies_available_in_books(book_title, books_df, copies_available)

    # Get the row index for the specific book
    book_row_index = books_df.index[books_df["title"] == book_title][0]

    # Retrieve the waiting_list queue
    waiting_list_str = books_df.at[book_row_index, "waiting_list"]

    # Calculate the length of the waiting list (number of names without commas)
    if waiting_list_str != "empty":
        requests = len(waiting_list_str.split(","))
    else:
        requests = 0

    # Retrieve the loaned_count for the book
    loaned_count = books_df.at[book_row_index, "loaned_count"]

    utils.check_and_update_book_in_popular_books(book_title, requests + loaned_count)

    update_loaned_count(book_title, books_df)

def alert_loaned_books(book_title, loaned_books_df,books_df, alert_label,tree):
    if book_title in loaned_books_df["title"].values:
        # Show inline error message
        alert_label.config(text=f"'{book_title}' is already loaned, putting you in a waiting list", fg="red")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds

        text = f"'{book_title}' is currently loaned out."
        client_name = utils.get_name_popup(text)

        if client_name:  # If a name is provided
            if utils.update_book_waiting_list(book_title, client_name, books_df, Paths.BOOKS.value):
                alert_label.config(text=f"Client '{client_name}' added to the waiting list of book '{book_title}'.", fg="green")
                alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
                # Reload the Treeview
                utils.load_books(tree, books_df)
        return True

    return False

@Logger.log_decorator("book borrowed successfully", "book borrowed fail")
def lend_selected_book(tree, alert_label):
    books_df, available_books_df, loaned_books_df = FileHandler.read_csv_files()

    selected_item = tree.selection()  # Get selected row
    if not selected_item:
        # Show inline error message
        alert_label.config(text="Please select a book to lend!", fg="red")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
        raise

    selected_values = tree.item(selected_item, "values")  # Get the row values
    book_title = selected_values[0]  # Assuming the first column is the title

    # Check if the book is already in loaned_books.csv
    if alert_loaned_books(book_title, loaned_books_df,books_df, alert_label, tree):
        raise

    # check if there is a waiting list for the book, then check if is the first in the waiting list
    if not check_waiting_list_name(book_title, alert_label, books_df):
        raise

    update_files(book_title)

    # Reload the data from the CSV files
    books_df, available_books_df, loaned_books_df = FileHandler.read_csv_files()

    # Reload the Treeview
    utils.load_books(tree, books_df)

    alert_label.config(text=f"'{book_title}' has been lend successfully!", fg="green")
    alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds


def open_lend_book_window():
    # Load books data from CSV
    try:
        books_df = pd.read_csv(Paths.BOOKS.value)
    except FileNotFoundError:
        tk.messagebox.showerror("Error", "Books file not found!")
        return

    # Create a new window
    lend_window = tk.Tk()
    utils.center_window(lend_window, 1000, 600)
    lend_window.title("Lend Book")
    lend_window.configure(bg="#f2f2f2")

    # Header
    header = tk.Label(lend_window, text="Lend Book", font=("Arial", 18, "bold"), bg="#4b0082", fg="white")
    header.pack(fill=tk.X, pady=(0, 10))

    # Inline Alert Label
    alert_label = tk.Label(lend_window, text="", font=("Arial", 12), bg="#f2f2f2")
    alert_label.pack()

    # lend book Button (at the top)
    lend_book_button = tk.Button(
        lend_window,
        text="Lend Selected Book",
        font=("Arial", 12, "bold"),
        bg="#4b0082",
        fg="white",
        command=lambda: lend_selected_book(tree, alert_label),
    )
    lend_book_button.pack(pady=10)

    # Treeview for displaying books
    columns = list(books_df.columns)  # Use the column names from the CSV
    tree = ttk.Treeview(lend_window, columns=columns, show="headings", height=15)
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Set up column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w", width=100)

    # Insert data into the Treeview
    utils.load_books(tree, books_df)

    # Close Button
    close_button = tk.Button(
        lend_window,
        text="Close",
        font=("Arial", 12, "bold"),
        bg="#4b0082",
        fg="white",
        command=lend_window.destroy,
    )
    close_button.pack(pady=10)

    # Start the Tkinter event loop
    lend_window.mainloop()
