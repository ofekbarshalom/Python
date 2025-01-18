import tkinter as tk
from tkinter import ttk
from helpers.utils import utils
from helpers.logger import Logger
from helpers.FileHandler import FileHandler


# Get the logger instance
log = Logger.get_logger()

@Logger.log_decorator("displayed successfully", "displayed fail")
def create_table(parent, data):
    """
        Create and display a table in a given window.
    """
    try:
        # Extract columns from the data
        columns = list(data.columns)

        # Create the Treeview widget
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Configure the column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="w", width=100)

        # Use the provided load_data_function to populate the table
        utils.load_books(tree, data)

    except Exception:
        raise

def open_popular_books_window():
    """
        Open a window displaying the popular books.
    """
    popular_books_df = FileHandler.read_popular_books_file()

    # Create a new window
    popular_window = tk.Tk()
    utils.center_window(popular_window, 800, 600)
    popular_window.title("Popular Books")
    popular_window.configure(bg="#f2f2f2")

    # Header
    header = tk.Label(popular_window, text="Popular Books", font=("Arial", 18, "bold"), bg="#4b0082", fg="white")
    header.pack(fill=tk.X, pady=(0, 10))

    create_table(popular_window, popular_books_df)

    # Close Button
    close_button = tk.Button(
        popular_window,
        text="Close",
        font=("Arial", 12, "bold"),
        bg="#4b0082",
        fg="white",
        command=popular_window.destroy,
    )
    close_button.pack(pady=10)

    # Start the Tkinter event loop
    popular_window.mainloop()
