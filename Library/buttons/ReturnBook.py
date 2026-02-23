import tkinter as tk
from tkinter import ttk
import pandas as pd
from helpers.FileHandler import FileHandler
from helpers.utils import utils
from helpers.path import Paths
from helpers.logger import Logger
from buttons.LendBook import check_book_request
from design.NotificationSystem import NotificationSystem

# Get the logger instance
log = Logger.get_logger()

def load_books(tree, books_df):
    """
        Load books data into the Treeview.
    """
    # Clear existing data in the Treeview
    for item in tree.get_children():
        tree.delete(item)
    # Insert new data
    for _, row in books_df.iterrows():
        tree.insert("", tk.END, values=list(row))


def add_book_to_available_books(book_title, available_books_df, copies_available):
    """
        Add a book to available_books.csv.
    """
    # Add the book to available_books.csv
    available_books_entry = pd.DataFrame({"title": [book_title], "copies_available": [copies_available]})
    available_books_df = pd.concat([available_books_df, available_books_entry], ignore_index=True)
    available_books_df.to_csv(Paths.AVAILABLE_BOOKS.value, index=False)
    # Print success message
    print(f"'{book_title}' has been added to available books!")

    return available_books_df


def remove_book_from_loaned_books(book_title, loaned_books_df):
    """
        Remove a book from loaned_books.csv.
    """
    # Remove the book from available_books.csv
    loaned_books_df = loaned_books_df[loaned_books_df["title"] != book_title]

    # Save the updated available_books.csv
    loaned_books_df.to_csv(Paths.LOANED_BOOKS.value, index=False)

    print(f"'{book_title}' has been removed from loaned_books.csv.")


def change_is_loaned(book_title,books_df):
    """
        Update the 'is_loaned' value of a book to 'No'.
    """
    # Update the is_loaned status to "Yes"
    books_df.loc[books_df["title"] == book_title, "is_loaned"] = "No"

    # Save the updated DataFrame back to the CSV file
    books_df.to_csv(Paths.BOOKS.value, index=False)

    print(f"'is_loaned' status for '{book_title}' has been updated to 'No'.")

    return books_df


def increment_copies_available_in_available_books(book_title, available_books_df, copies_available):
    """
        Increment the available_copies value  of a book in available_books.csv.
    """
    # Decrement copies_available for the book in available_books.csv
    available_books_df.loc[available_books_df["title"] == book_title, "copies_available"] += 1

    # Save the updated available_books.csv
    available_books_df.to_csv(Paths.AVAILABLE_BOOKS.value, index=False)

def increment_copies_available_in_books(book_title, books_df, copies_available):
    """
        Increment the available_copies value of a book in books.csv.
    """
    # Decrement copies_available in books.csv
    books_df.loc[books_df["title"] == book_title, "copies_available"] += 1

    # Save the updated books.csv
    books_df.to_csv(Paths.BOOKS.value, index=False)

def update_files(book_title):
    """
        Update the data files when a book is returned.
    """
    books_df, available_books_df, loaned_books_df = FileHandler.read_csv_files()

    # Find the book in books_df and get the copies_available
    try:
        book_data = books_df.loc[books_df["title"] == book_title]
        copies_available = int(book_data["copies_available"].values[0])
    except IndexError:
        print(f"Book '{book_title}' not found in the main books.csv!")
        return

    if copies_available == 0:
        available_books_df = add_book_to_available_books(book_title, available_books_df, copies_available)
        remove_book_from_loaned_books(book_title, loaned_books_df)
        books_df = change_is_loaned(book_title, books_df)

    # increment copies_available in files
    increment_copies_available_in_books(book_title, books_df, copies_available)
    increment_copies_available_in_available_books(book_title, available_books_df, copies_available)

    books_waiting_list_first_name = check_book_request(book_title, books_df)

    if books_waiting_list_first_name:
        message = f"{books_waiting_list_first_name} can lend the book {book_title} now"
        utils.add_message_to_users(message)

def alert_returned_books(book_title, books_df, alert_label):
    """
        Alert if all copies of a book have already been returned.
    """
    # Find the book in books_df and get the copies_available
    try:
        book_data = books_df.loc[books_df["title"] == book_title]
        copies_available = int(book_data["copies_available"].values[0])
        copies = int(book_data["copies"].values[0])
    except IndexError:
        print(f"Book '{book_title}' not found in the main books.csv!")
        return

    if copies_available == copies:
        # Show inline error message
        alert_label.config(text=f"All copies of '{book_title}' are already returned", fg="red")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
        return True

    return False


@Logger.log_decorator("book returned successfully", "book returned fail")
def return_selected_book(tree, alert_label):
    """
        Process the return of a selected book using helper methods.
    """
    books_df, available_books_df, loaned_books_df = FileHandler.read_csv_files()

    selected_item = tree.selection()  # Get selected row
    if not selected_item:
        # Show inline error message
        alert_label.config(text="Please select a book to lend!", fg="red")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
        raise

    selected_values = tree.item(selected_item, "values")  # Get the row values
    book_title = selected_values[0]  # Assuming the first column is the title

    #  Check if all the copies are loaned
    if alert_returned_books(book_title, books_df, alert_label):
        raise

    update_files(book_title)

    # Reload the data from the CSV files
    books_df, available_books_df, loaned_books_df = FileHandler.read_csv_files()

    # Reload the Treeview
    load_books(tree, books_df)

    alert_label.config(text=f"'{book_title}' has been returned successfully!", fg="green")
    alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds


def open_return_book_window():
    """
        Open the 'Return Book' window for processing book returns.
    """
    books_df, _, _ = FileHandler.read_csv_files()

    # Create a new window
    return_window = tk.Tk()
    utils.center_window(return_window, 1000, 600)
    return_window.title("Return Book")
    return_window.configure(bg="#f2f2f2")

    # Header
    header = tk.Label(return_window, text="Return Book", font=("Arial", 18, "bold"), bg="#4b0082", fg="white")
    header.pack(fill=tk.X, pady=(0, 10))

    # Inline Alert Label
    alert_label = tk.Label(return_window, text="", font=("Arial", 12), bg="#f2f2f2")
    alert_label.pack()

    # Remove Button (at the top)
    return_book_button = tk.Button(
        return_window,
        text="Return Selected Book",
        font=("Arial", 12, "bold"),
        bg="#4b0082",
        fg="white",
        command=lambda: return_selected_book(tree, alert_label),
    )
    return_book_button.pack(pady=10)

    # Treeview for displaying books
    columns = list(books_df.columns)  # Use the column names from the CSV
    tree = ttk.Treeview(return_window, columns=columns, show="headings", height=15)
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Set up column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w", width=100)

    # Insert data into the Treeview
    load_books(tree, books_df)

    # Close Button
    close_button = tk.Button(
        return_window,
        text="Close",
        font=("Arial", 12, "bold"),
        bg="#4b0082",
        fg="white",
        command=return_window.destroy,
    )
    close_button.pack(pady=10)

    # Start the Tkinter event loop
    return_window.mainloop()
