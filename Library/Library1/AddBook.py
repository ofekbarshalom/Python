import tkinter as tk
from Librarian import Librarian
from BookFactory import *

def center_window(window, width, height):
    # Get the screen's width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window's geometry to center it
    window.geometry(f"{width}x{height}+{x}+{y}")


def submit_new_book(entries, dropdown_var, current_window, refresh_callback):
    # Extract book details from the entries
    title = entries["title"].get()
    author = entries["author"].get()
    is_loaned = dropdown_var.get()
    copies = entries["copies"].get()
    genre = entries["genre"].get()
    year = entries["year"].get()

    # Validate and convert fields
    copies = int(copies) if copies.isdigit() else 1
    year = int(year) if year and year.isdigit() else None

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
    Librarian.add_book_to_library(new_book)

    # Refresh the table in the library
    if refresh_callback:
        refresh_callback()

    # Print book details (optional debug output)
    print(f"New Book Created: {new_book}")

    # Close the current window
    current_window.destroy()


def open_add_new_book_window(refresh_callback):
    # Main window setup
    new_book_window = tk.Tk()
    center_window(new_book_window, 500, 600)
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

    # Submit button (Regular rectangular button)
    submit_button = tk.Button(
        form_frame,
        text="Submit",
        font=("Arial", 14, "bold"),
        bg="#4b0082",
        fg="white",
        width=20,
        command=lambda: submit_new_book(entries, dropdown_var, new_book_window, refresh_callback),
    )
    submit_button.pack(pady=20)

    # Start the Tkinter loop
    new_book_window.mainloop()

