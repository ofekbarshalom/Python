import tkinter as tk
from tkinter import ttk
from components.RoundedButton import RoundedButton
from AddBook import open_add_new_book_window
from path import Paths
import csv


def center_window(window, width, height):
    # Get the screen's width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window's geometry to center it
    window.geometry(f"{width}x{height}+{x}+{y}")


def refresh_table(table):
    """Refresh the table with updated data from 'books.csv'."""
    # Clear existing rows
    for row in table.get_children():
        table.delete(row)

    # Repopulate the table with updated data
    try:
        with open(Paths.BOOKS.value, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                table.insert("", tk.END, values=(row["title"], row["author"], row["is_loaned"], row["copies"], row["genre"], row["year"]))
    except FileNotFoundError:
        print("books.csv not found. Please make sure the file exists.")

def dummy_command(action):
    print(f"{action} button clicked!")


def open_library_window():
    # Main window setup
    root = tk.Tk()
    center_window(root, 1000, 700)
    root.title("Library")
    root.configure(bg="#f2f2f2")

    # Header
    header = tk.Label(root, text="Library", font=("Arial", 24, "bold"), bg="#4b0082", fg="white")
    header.pack(fill=tk.X, pady=(0, 10))

    # Search Bar Frame
    search_frame = tk.Frame(root, bg="#f2f2f2")
    search_frame.pack(pady=(0, 10))

    search_icon = tk.Label(search_frame, text="🔍", font=("Arial", 16), bg="#f2f2f2", fg="#4b0082")
    search_icon.pack(side=tk.LEFT, padx=(10, 5))
    search_entry = tk.Entry(search_frame, font=("Arial", 14), width=50)
    search_entry.pack(side=tk.LEFT, padx=(0, 10))
    search_button = tk.Button(
        search_frame, text="Search Book", font=("Arial", 12), bg="#4b0082", fg="white", command=lambda: dummy_command("Search")
    )
    search_button.pack(side=tk.LEFT)

    # Buttons Frame
    buttons_frame = tk.Frame(root, bg="#f2f2f2")
    buttons_frame.pack(pady=(10, 10))

    # Table Frame
    table_frame = tk.Frame(root, bg="#f2f2f2")
    table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Scrollable Table (Treeview)
    table = ttk.Treeview(table_frame, columns=("Title", "Author", "Is Loaned", "Copies", "Genre", "Year"), show="headings")
    table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Define Table Headings
    table.heading("Title", text="Title")
    table.heading("Author", text="Author")
    table.heading("Is Loaned", text="Is Loaned")
    table.heading("Copies", text="Copies")
    table.heading("Genre", text="Genre")
    table.heading("Year", text="Year")

    # Scrollbar for Table
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Populate Table with Data from 'books.csv'
    refresh_table(table)

    # Buttons Data with Actions
    buttons = [
        ("Add Book", lambda: open_add_new_book_window(lambda: refresh_table(table))),
        ("Remove Book", dummy_command),
        ("View Books", dummy_command),
        ("Lend Book", dummy_command),
        ("Return Book", dummy_command),
        ("Logout", dummy_command),
        ("Login", dummy_command),
        ("Register", dummy_command),
        ("Popular Books", dummy_command),
    ]

    # Create buttons in two rows
    for idx, (label, action) in enumerate(buttons):
        row = idx // 5
        col = idx % 5
        button = tk.Button(
            buttons_frame,
            text=label,
            font=("Arial", 12, "bold"),
            bg="#4b0082",
            fg="white",
            width=15,
            command=action,
        )
        button.grid(row=row, column=col, padx=10, pady=10)

    # Start the Tkinter event loop
    root.mainloop()
