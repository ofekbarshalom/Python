import tkinter as tk
from tkinter import ttk
from path import Paths
from utils import utils
import csv
from logger import Logger

log = Logger.get_logger()  # Get the logger instance

# Strategy Pattern for Searching
class SearchStrategy:
    def search(self, query, books):
        raise NotImplementedError("Search method not implemented")

class SearchByTitle(SearchStrategy):
    def search(self, query, books):
        result = []
        for book in books:  # Loop through each book in the list of books
            if book["title"].lower().startswith(query.lower()):
                result.append(book)
        return result

class SearchByAuthor(SearchStrategy):
    def search(self, query, books):
        result = []
        for book in books:  # Loop through each book in the list of books
            if book["author"].lower().startswith(query.lower()):
                result.append(book)
        return result

class SearchByGenre(SearchStrategy):
    def search(self, query, books):
        result = []
        for book in books:  # Loop through each book in the list of books
            if book["genre"].lower().startswith(query.lower()):
                result.append(book)
        return result

# Helper to load books from CSV
def load_books():
    try:
        with open(Paths.BOOKS.value, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []

# Helper to refresh the table
def refresh_table(table, books):
    table.delete(*table.get_children())  # Clear table rows
    for book in books:
        table.insert(
            "",
            tk.END,
            values=(book["title"], book["author"], book["is_loaned"], book["copies"], book["genre"], book["year"])
        )


# Function to perform search
@Logger.log_search()
def perform_search(search_entry, search_type_combobox, table):
    query = search_entry.get()
    search_type = search_type_combobox.get()
    books = load_books()

    # Select the appropriate strategy
    if search_type == "Title":
        strategy = SearchByTitle()
    elif search_type == "Author":
        strategy = SearchByAuthor()
    elif search_type == "Genre":
        strategy = SearchByGenre()
    else:
        strategy = None

    # Perform the search and refresh the table
    if strategy:
        results = strategy.search(query, books)
        refresh_table(table, results)

# Main function to open the Search Books window
def open_search_books_window():
    # Create the main window for searching books
    search_books_window = tk.Tk()

    # Use the center_window function to center the window
    utils.center_window(search_books_window, 1000, 700)

    search_books_window.title("Search Books")
    search_books_window.configure(bg="#f2f2f2")

    # Header
    header_label = tk.Label(
        search_books_window,
        text="Search Books",
        font=("Arial", 20, "bold"),
        bg="#4b0082",
        fg="white"
    )
    header_label.pack(fill=tk.X, pady=(0, 10))

    # Search Bar Frame
    search_frame = tk.Frame(search_books_window, bg="#f2f2f2")
    search_frame.pack(pady=(0, 10))

    # Search Query Label and Entry
    search_label = tk.Label(
        search_frame,
        text="Search Query:",
        font=("Arial", 14),
        bg="#f2f2f2",
        fg="#4b0082"
    )
    search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    search_entry = tk.Entry(search_frame, font=("Arial", 14), width=30)
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    # Search Type Label and Combobox
    search_type_label = tk.Label(
        search_frame,
        text="Search By:",
        font=("Arial", 14),
        bg="#f2f2f2",
        fg="#4b0082"
    )
    search_type_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
    search_type_combobox = ttk.Combobox(
        search_frame,
        font=("Arial", 14),
        values=["Title", "Author", "Genre"],
        state="readonly"
    )
    search_type_combobox.grid(row=0, column=3, padx=5, pady=5)
    search_type_combobox.set("Title")  # Default selection

    # Search Button
    search_button = tk.Button(
        search_frame,
        text="Search",
        font=("Arial", 14, "bold"),
        bg="#4b0082",
        fg="white",
        command=lambda: perform_search(search_entry, search_type_combobox, table)
    )
    search_button.grid(row=0, column=4, padx=5, pady=5)

    # Table Frame
    table_frame = tk.Frame(search_books_window, bg="#f2f2f2")
    table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Scrollable Table (Treeview)
    table = ttk.Treeview(
        table_frame,
        columns=("Title", "Author", "Is Loaned", "Copies", "Genre", "Year"),
        show="headings"
    )
    table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Define Table Headings
    table.heading("Title", text="Title")
    table.heading("Author", text="Author")
    table.heading("Is Loaned", text="Is Loaned")
    table.heading("Copies", text="Copies")
    table.heading("Genre", text="Genre")
    table.heading("Year", text="Year")

    # Add a vertical scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Close Button
    close_button = tk.Button(
        search_books_window,
        text="Close",
        font=("Arial", 14, "bold"),
        bg="#4b0082",
        fg="white",
        command=search_books_window.destroy
    )
    close_button.pack(pady=10)

    search_books_window.mainloop()
