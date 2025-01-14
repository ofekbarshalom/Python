import tkinter as tk
from tkinter import ttk
from helpers.utils import utils
from helpers.logger import Logger
from abc import ABC, abstractmethod
from helpers.FileHandler import FileHandler

log = Logger.get_logger()  # Get the logger instance

# Strategy Pattern for Searching
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, query, books):
        pass

class SearchByTitle(SearchStrategy):
    def search(self, query, books_df):
        return books_df[books_df["title"].str.lower().str.startswith(query.lower(), na=False)]

class SearchByAuthor(SearchStrategy):
    def search(self, query, books_df):
        return books_df[books_df["author"].str.lower().str.startswith(query.lower(), na=False)]

class SearchByGenre(SearchStrategy):
    def search(self, query, books_df):
        return books_df[books_df["genre"].str.lower().str.startswith(query.lower(), na=False)]
# Helper to refresh the table
def refresh_table(table, books_df):
    table.delete(*table.get_children())  # Clear table rows
    for _, book in books_df.iterrows():
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
    books_df,_,_ = FileHandler.read_csv_files()

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
        results = strategy.search(query, books_df)
        refresh_table(table, results)

# Main function to open the Search Books window
def open_search_books_window():
    # Create the start window for searching books
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

    # Define Table Headings and Set Equal Column Widths
    column_width = 150  # Set a uniform width for all columns
    for col in ["Title", "Author", "Is Loaned", "Copies", "Genre", "Year"]:
        table.heading(col, text=col)
        table.column(col, width=column_width)

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
