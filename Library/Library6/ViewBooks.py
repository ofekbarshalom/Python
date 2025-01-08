import tkinter as tk
from tkinter import ttk
from path import Paths
import csv
from utils import utils


def load_books_from_file(file_path):
    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return None

def refresh_table(table, file_path):
    table.delete(*table.get_children())
    books = load_books_from_file(file_path)

    if books is None:
        table.insert("", tk.END, values=("Error: File not found!",))
    else:
        for book in books:
            table.insert("", tk.END, values=tuple(book.values()))

def update_table_columns(table, file_path):
    # Clear existing table data and columns
    table.delete(*table.get_children())
    for col in table["columns"]:
        table.heading(col, text="")
        table.column(col, width=0)

    # Load new data and update table structure
    books = load_books_from_file(file_path)
    if books:
        columns = list(books[0].keys())
        table["columns"] = columns

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=150)

        # Populate table with new data
        refresh_table(table, file_path)
    else:
        table["columns"] = ("Error",)
        table.heading("Error", text="Error")
        table.column("Error", width=200)
        table.insert("", tk.END, values=("Error: File not found!",))


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

    file_options = {
        "All Books": Paths.BOOKS.value,
        "Available Books": Paths.AVAILABLE_BOOKS.value,
        "Loaned Books": Paths.LOANED_BOOKS.value,
    }
    selected_file = tk.StringVar(value="All Books")

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

    # Bind event to update table when dropdown value changes
    file_selector.bind("<<ComboboxSelected>>",
                       lambda event: update_table_columns(table, file_options[selected_file.get()]))

    refresh_button = tk.Button(
        dropdown_frame,
        text="Refresh",
        font=("Arial", 14, "bold"),
        bg="#4b0082",
        fg="white",
        command=lambda: update_table_columns(table, file_options[selected_file.get()])
    )
    refresh_button.pack(side=tk.LEFT, padx=(10, 0))

    print(f"Selected file: {selected_file.get()}")
    print(f"File path: {file_options[selected_file.get()]}")

    close_button = tk.Button(
        view_books_window,
        text="Close",
        font=("Arial", 14, "bold"),
        bg="#4b0082",
        fg="white",
        command=view_books_window.destroy
    )
    close_button.pack(pady=10)

    update_table_columns(table, file_options[selected_file.get()])

    view_books_window.mainloop()
