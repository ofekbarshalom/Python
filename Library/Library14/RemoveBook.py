import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from utils import utils
from path import Paths
from logger import Logger

# Get the logger instance
log = Logger.get_logger()

def load_books(tree, books_df):
    # Clear existing data in the Treeview
    for item in tree.get_children():
        tree.delete(item)
    # Insert new data
    for _, row in books_df.iterrows():
        tree.insert("", tk.END, values=list(row))

@Logger.log_decorator("book removed successfully", "book removed fail")
def remove_selected_book(tree, books_df, alert_label):
    selected_item = tree.selection()  # Get selected row
    if not selected_item:
        # Show inline error message
        alert_label.config(text="Please select a book to remove!", fg="red")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
        log.error("book removed fail")
        return

    selected_values = tree.item(selected_item, "values")  # Get the row values
    book_title = selected_values[0]  # Assuming the first column is the title

    copies, copies_available = books_df.loc[books_df["title"] == book_title, ["copies", "copies_available"]].values[0]

    if copies == copies_available:

        # Remove the book from the DataFrame
        books_df = books_df[books_df["title"] != book_title]

        # Update loaned_books.csv
        try:
            loaned_books_df = pd.read_csv(Paths.LOANED_BOOKS.value)  # Path to loaned_books.csv
            updated_loaned_books_df = loaned_books_df[loaned_books_df["title"] != book_title]
            updated_loaned_books_df.to_csv(Paths.LOANED_BOOKS.value, index=False)
        except FileNotFoundError:
            pass  # If the file doesn't exist, do nothing

        # Update available_books.csv
        try:
            available_books_df = pd.read_csv(Paths.AVAILABLE_BOOKS.value)  # Path to available_books.csv
            updated_available_books_df = available_books_df[available_books_df["title"] != book_title]
            updated_available_books_df.to_csv(Paths.AVAILABLE_BOOKS.value, index=False)
        except FileNotFoundError:
            pass  # If the file doesn't exist, do nothing

        # Save the updated DataFrame back to the CSV file
        books_df.to_csv(Paths.BOOKS.value, index=False)

        alert_label.config(text=f"'{book_title}' has been removed successfully!", fg="green")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
    else:
        alert_label.config(text=f"'{book_title}' has copies that are not returned yet", fg="red")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
        raise

    # Reload the Treeview
    load_books(tree, books_df)

def open_remove_book_window():
    # Load books data from CSV
    try:
        books_df = pd.read_csv(Paths.BOOKS.value)
    except FileNotFoundError:
        tk.messagebox.showerror("Error", "Books file not found!")
        return

    # Create a new window
    remove_window = tk.Tk()
    utils.center_window(remove_window, 800, 600)
    remove_window.title("Remove Book")
    remove_window.configure(bg="#f2f2f2")

    # Header
    header = tk.Label(remove_window, text="Remove Book", font=("Arial", 18, "bold"), bg="#4b0082", fg="white")
    header.pack(fill=tk.X, pady=(0, 10))

    # Inline Alert Label
    alert_label = tk.Label(remove_window, text="", font=("Arial", 12), bg="#f2f2f2")
    alert_label.pack()

    # Remove Button (at the top)
    remove_button = tk.Button(
        remove_window,
        text="Remove Selected Book",
        font=("Arial", 12, "bold"),
        bg="#4b0082",
        fg="white",
        command=lambda: remove_selected_book(tree, books_df, alert_label),
    )
    remove_button.pack(pady=10)

    # Treeview for displaying books
    columns = list(books_df.columns)  # Use the column names from the CSV
    tree = ttk.Treeview(remove_window, columns=columns, show="headings", height=15)
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Set up column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w", width=100)

    # Insert data into the Treeview
    load_books(tree, books_df)

    # Close Button
    close_button = tk.Button(
        remove_window,
        text="Close",
        font=("Arial", 12, "bold"),
        bg="#4b0082",
        fg="white",
        command=remove_window.destroy,
    )
    close_button.pack(pady=10)

    # Start the Tkinter event loop
    remove_window.mainloop()
