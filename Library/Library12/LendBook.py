import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from FileHandler import FileHandler
from Books_dict import *
from utils import utils
from path import Paths
from Book import Book
from logger import Logger

# Get the logger instance
log = Logger.get_logger()

#debug function
def print_queue(queue):
    if queue.empty():
        print("The queue is empty.")
    else:
        print("Queue contents:", list(queue.queue))


def load_books(tree, books_df):
    # Clear existing data in the Treeview
    for item in tree.get_children():
        tree.delete(item)
    # Insert new data
    for _, row in books_df.iterrows():
        tree.insert("", tk.END, values=list(row))

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


def check_book_request(book_title):
    book = get_book_object(book_title)

    if book:
        print(f"queue:{book_title}")  # debug
        print_queue(book.client_queue)  # debug
        if not book.client_queue.empty():
            # Peek the top of the queue without removing the item
            first_request = book.client_queue.queue[0]  # Access the first item directly
            return first_request
        return None
    return None

def remove_first_request(book_title):
    book = get_book_object(book_title)
    if book:
        if not book.client_queue.empty():
            book.client_queue.get()  # Access the first item directly
            book.request -= 1
            chack_book_in_popular_books(book_title, book.request + book.loaned_count)

    print(f"queue after removing:{book_title}")  # debug
    print_queue(book.client_queue)  # debug

def check_waiting_list_name(book_title, alert_label):
    first_in_queue = check_book_request(book_title)

    if first_in_queue:
        text = f"'{book_title}' has a waiting list.\nIf you're first, the book will be loaned to you."
        client_name = utils.get_name_popup(text)

        if client_name == first_in_queue:
            remove_first_request(book_title)
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

    book = get_book_object(book_title)
    book.loaned_count += 1

    check_and_update_book_in_popular_books(book_title, book.loaned_count + book.request)

def alert_loaned_books(book_title, loaned_books_df, alert_label):
    if book_title in loaned_books_df["title"].values:
        # Show inline error message
        alert_label.config(text=f"'{book_title}' is already loaned, putting you in a waiting list", fg="red")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds

        text = f"'{book_title}' is currently loaned out."
        client_name = utils.get_name_popup(text)

        if client_name:  # If a name is provided
            if update_book_waiting_list(book_title, client_name):
                alert_label.config(text=f"Client '{client_name}' added to the waiting list of book '{book_title}'.", fg="green")
                alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
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
    if alert_loaned_books(book_title, loaned_books_df, alert_label):
        raise

    # check if there is a waiting list for the book, then check if is the first in the waiting list
    if not check_waiting_list_name(book_title, alert_label):
        raise

    update_files(book_title)

    # Reload the data from the CSV files
    books_df, available_books_df, loaned_books_df = FileHandler.read_csv_files()

    # Reload the Treeview
    load_books(tree, books_df)

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
    utils.center_window(lend_window, 800, 600)
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
    load_books(tree, books_df)

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
