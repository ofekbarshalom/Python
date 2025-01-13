import tkinter as tk
from User import User
from BookFactory import BookFactory
from FileHandler import *
from logger import Logger
from utils import utils
from NotificationSystem import NotificationSystem

# Get the logger instance
log = Logger.get_logger()

def check_copies_and_year(copies, year, alert_label):
    try:
        # Validate and convert fields
        copies = int(copies)
        if copies <= 0:
            alert_label.config(text="Copies must be a positive integer.", fg="red")
            alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
            raise ValueError("Copies must be a positive integer.")

        year = int(year)
    except ValueError:
        alert_label.config(text="copies and year most be a number", fg="red")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
        raise ValueError("Copies and year must be a number.")

@Logger.log_decorator("Book added successfully", "Book added fail")
def submit_new_book(entries, dropdown_var, current_window, alert_label):
    # Extract book details from the entries
    title = entries["title"].get()
    author = entries["author"].get()
    is_loaned = dropdown_var.get()
    copies = entries["copies"].get()
    genre = entries["genre"].get()
    year = entries["year"].get()

    # Check if required fields are filled
    if not title or not author or not copies or not genre or not year:
        # Show inline error message
        alert_label.config(text="All fields must be filled out!", fg="red")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds
        raise ValueError("Missing required fields.")

    check_copies_and_year(copies,year, alert_label)

    # Create the book using BookFactory
    new_book = BookFactory.create_book(
        title=title,
        author=author,
        is_loaned=is_loaned,
        copies=copies,
        genre=genre,
        year=year,
    )

    # Add the book to the library
    User.add_book_to_library(new_book)

    users_df = FileHandler.read_users_file()

    message = f"The book {title} added to the library"

    notification_system = NotificationSystem.get_instance()
    notification_system.notify_observers(message, users_df)

    # Close the current window
    current_window.destroy()


def open_add_new_book_window():
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
