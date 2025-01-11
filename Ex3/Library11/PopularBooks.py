import tkinter as tk
from tkinter import ttk
import pandas as pd
from utils import utils
from path import Paths

def load_books(tree, books_df):
    # Clear existing data in the Treeview
    for item in tree.get_children():
        tree.delete(item)
    # Insert new data
    for _, row in books_df.iterrows():
        tree.insert("", tk.END, values=list(row))

def open_popular_books_window():
    # Load popular_books data from CSV
    try:
        popular_books_df = pd.read_csv(Paths.POPULAR_BOOKS.value)  # Path to popular_books.csv
    except FileNotFoundError:
        tk.messagebox.showerror("Error", "Popular books file not found!")
        return

    # Create a new window
    popular_window = tk.Tk()
    utils.center_window(popular_window, 800, 600)
    popular_window.title("Popular Books")
    popular_window.configure(bg="#f2f2f2")

    # Header
    header = tk.Label(popular_window, text="Popular Books", font=("Arial", 18, "bold"), bg="#4b0082", fg="white")
    header.pack(fill=tk.X, pady=(0, 10))

    # Treeview for displaying popular books
    columns = list(popular_books_df.columns)  # Use the column names from the CSV
    tree = ttk.Treeview(popular_window, columns=columns, show="headings", height=15)
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Set up column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w", width=100)

    # Insert data into the Treeview
    load_books(tree, popular_books_df)

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
