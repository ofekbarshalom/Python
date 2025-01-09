import tkinter as tk
from tkinter import ttk
import pandas as pd  # Use Pandas for better CSV handling
from path import Paths
from utils import utils


def load_books_from_file(file_path):
    try:
        # Load CSV into a Pandas DataFrame
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")  # Notify if file is missing
        return None


def update_table_with_pandas(table, file_path):
    # Clear all existing columns and data from the table
    table.delete(*table.get_children())
    table["columns"] = []

    # Load the CSV file with Pandas
    df = load_books_from_file(file_path)
    if df is not None and not df.empty:
        # Set columns dynamically
        columns = list(df.columns)
        table["columns"] = columns

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=150)

        # Insert rows into the table
        for _, row in df.iterrows():
            table.insert("", tk.END, values=list(row))
    else:
        table["columns"] = ("Error",)
        table.heading("Error", text="Error")
        table.column("Error", width=200)
        table.insert("", tk.END, values=("Error: File not found or empty!",))


def open_view_books_window():
    view_books_window = tk.Tk()
    utils.center_window(view_books_window, 800, 600)
    view_books_window.title("View Books")
    view_books_window.configure(bg="#f2f2f2")

    header_label = tk.Label(
        view_books_window,
        text="Books in Library",
        font=("Arial", 20, "bold"),
        bg="#4b0082",
        fg="white"
    )
    header_label.pack(fill=tk.X, pady=(0, 10))

    dropdown_frame = tk.Frame(view_books_window, bg="#f2f2f2")
    dropdown_frame.pack(pady=(0, 10))

    dropdown_label = tk.Label(
        dropdown_frame,
        text="Select File:",
        font=("Arial", 14),
        bg="#f2f2f2",
        fg="#4b0082"
    )
    dropdown_label.pack(side=tk.LEFT, padx=(10, 5))

    # Define file options
    file_options = {
        "All Books": Paths.BOOKS.value,
        "Available Books": Paths.AVAILABLE_BOOKS.value,
        "Loaned Books": Paths.LOANED_BOOKS.value,
    }

    selected_file = tk.StringVar(value="All Books")  # Default for dropdown
    file_selector = ttk.Combobox(
        dropdown_frame,
        textvariable=selected_file,
        font=("Arial", 14),
        values=list(file_options.keys()),
        state="readonly"
    )
    file_selector.pack(side=tk.LEFT, padx=(0, 10))

    table_frame = tk.Frame(view_books_window, bg="#f2f2f2")
    table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    table = ttk.Treeview(table_frame, show="headings")
    table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_table():
        selected_option = file_selector.get()  # Fetch current dropdown value
        if not selected_option:
            print("No file selected!")  # Notify if no file is selected
            return
        file_path = file_options.get(selected_option)  # Match dropdown value to path
        if file_path:
            update_table_with_pandas(table, file_path)
        else:
            print(f"Invalid selection: {selected_option}")  # Notify if invalid selection

    refresh_button = tk.Button(
        dropdown_frame,
        text="Refresh",
        font=("Arial", 14, "bold"),
        bg="#4b0082",
        fg="white",
        command=refresh_table  # Call refresh_table on button click
    )
    refresh_button.pack(side=tk.LEFT, padx=(10, 0))

    close_button = tk.Button(
        view_books_window,
        text="Close",
        font=("Arial", 14, "bold"),
        bg="#4b0082",
        fg="white",
        command=view_books_window.destroy
    )
    close_button.pack(pady=10)

    # Populate the table with the default file's data on startup
    default_file_path = file_options.get("All Books")  # Default to "All Books"
    update_table_with_pandas(table, default_file_path)

    view_books_window.mainloop()
