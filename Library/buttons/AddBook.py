import os
import tkinter as tk
from design.User import User
from start.BookFactory import BookFactory
from helpers.FileHandler import FileHandler
from helpers.logger import Logger
from helpers.utils import utils
from design.NotificationSystem import NotificationSystem
from buttons.LendBook import add_book_to_loaned_books

# Get the logger instance
log = Logger.get_logger()

def check_book_title(book_title):
    """
        Check if a book title exists in the library.
    """
    # Read the books data
    books_df, _, _ = FileHandler.read_csv_files()

    exists = books_df['title'].str.lower().eq(book_title.lower()).any()
    return exists


def check_copies_and_year(copies, year, alert_label):
    """
        Validate if copies and year are positive integers.
    """
    try:
        # Validate and convert copies
        copies = int(copies)
        if copies <= 0:
            alert_label.config(text="Copies must be a positive integer.", fg="red")
            alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
            raise ValueError("Copies must be a positive integer.")

        # Validate and convert year
        year = int(year)

    except ValueError as e:
        # If the error was not raised explicitly above, it's likely due to non-integer input
        if "invalid literal" in str(e):
            alert_label.config(text="Copies and year must be numbers.", fg="red")
            alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
            raise ValueError("Copies and year must be numbers.")
        else:
            raise  # Re-raise the specific errors

def validate_required_fields(entries, alert_label):
    """
    Validate if all required fields are filled.
    """
    # Extract fields
    title = entries["title"].get()
    author = entries["author"].get()
    copies = entries["copies"].get()
    genre = entries["genre"].get()
    year = entries["year"].get()

    # Check if any required field is empty
    if not title or not author or not copies or not genre or not year:
        alert_label.config(text="All fields must be filled out!", fg="red")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
        raise ValueError("Missing required fields.")

    # Return fields for further use
    return title, author, copies, genre, year


@Logger.log_decorator("Book added successfully", "Book added fail")
def submit_new_book(entries, dropdown_var, current_window, alert_label):
    """
       Submit a new book to the library after validation with helper methods.
    """
    # Validate required fields
    title, author, copies, genre, year = validate_required_fields(entries, alert_label)

    # Extract additional details
    is_loaned = dropdown_var.get()

    check_copies_and_year(copies,year, alert_label)

    # check if there is a book with this name already
    if check_book_title(title):
        # Display a message to the user
        alert_label.config(text="Book title already exists!", fg="red")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
        raise ValueError(f"The book '{title}' already exists in the database.")

    # Create the book using BookFactory
    new_book = BookFactory.create_book(title,author,is_loaned,copies,genre,year)

    # Add the book to the library
    User.add_book_to_library(new_book)

    if is_loaned == "Yes":
        _, _, loaned_books_df = FileHandler.read_csv_files()
        add_book_to_loaned_books(title,loaned_books_df)

    message = f"The book {title} added to the library"
    utils.add_message_to_users(message)

    # Show the alert message
    alert_label.config(text=f"The book {title} added to the library", fg="green")

    # Schedule the window to close after 2 seconds
    current_window.after(1000, current_window.destroy)


def open_add_new_book_window():
    """
        Create and display the "Add New Book" window.
    """
    # Main window setup
    new_book_window = tk.Tk()
    utils.center_window(new_book_window, 500, 620)
    new_book_window.title("Library/Add New Book")
    new_book_window.configure(bg="#f2f2f2")  # Light gray background

    # Header
    header = tk.Label(new_book_window, text="Add New Book", font=("Arial", 24, "bold"), bg="#4b0082", fg="white")
    header.pack(fill=tk.X, pady=(0, 20))  # Purple header

    # Form frame
    form_frame = tk.Frame(new_book_window, bg="#f2f2f2")
    form_frame.pack(pady=10)

    # Input fields
    labels = ["Title:", "Author:", "Copies:", "Genre:", "Year:"]
    entries = {}
    for label_text in labels:
        label = tk.Label(form_frame, text=label_text, font=("Arial", 14), bg="#f2f2f2", fg="#4b0082")
        label.pack(anchor="w", pady=(5, 0))  # Place label above the input with some spacing
        entry = tk.Entry(form_frame, font=("Arial", 14), width=30)
        entry.pack(pady=(0, 10))  # Spacing below the input field
        entries[label_text[:-1].lower()] = entry  # Save entries with lowercase keys

    # Dropdown for "Is Loaned"
    dropdown_label = tk.Label(form_frame, text="Is Loaned (Yes/No):", font=("Arial", 14), bg="#f2f2f2", fg="#4b0082")
    dropdown_label.pack(anchor="w", pady=(5, 0))

    dropdown_var = tk.StringVar()
    dropdown_var.set("No")  # Default value
    dropdown_menu = tk.OptionMenu(form_frame, dropdown_var, "Yes", "No")
    dropdown_menu.config(font=("Arial", 14), bg="white", fg="black", width=28)
    dropdown_menu.pack(pady=(0, 10))

    # Inline Alert Label
    alert_label = tk.Label(new_book_window, text="", font=("Arial", 12), bg="#f2f2f2")
    alert_label.pack()

    # Submit button (Regular rectangular button)
    submit_button = tk.Button(
        form_frame,
        text="Submit",
        font=("Arial", 14, "bold"),
        bg="#4b0082",
        fg="white",
        width=20,
        command=lambda: submit_new_book(entries, dropdown_var, new_book_window, alert_label),
    )
    submit_button.pack(pady=20)

    # Start the Tkinter loop
    new_book_window.mainloop()
