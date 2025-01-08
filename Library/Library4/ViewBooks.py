import tkinter as tk
from tkinter import ttk
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

def open_view_books_window():
    # Create the main window for viewing books
    view_books_window = tk.Tk()
    center_window(view_books_window, 800, 600)
    view_books_window.title("View Books")
    view_books_window.configure(bg="#f2f2f2")

    # Header
    header_label = tk.Label(
        view_books_window,
        text="Books in Library",
        font=("Arial", 20, "bold"),
        bg="#4b0082",
        fg="white"
    )
    header_label.pack(fill=tk.X, pady=(0, 10))

    # Table Frame
    table_frame = tk.Frame(view_books_window, bg="#f2f2f2")
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

    # Populate the table with data from books.csv
    try:
        with open(Paths.BOOKS.value, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                table.insert(
                    "",
                    tk.END,
                    values=(
                        row["title"],
                        row["author"],
                        row["is_loaned"],
                        row["copies"],
                        row["genre"],
                        row["year"]
                    )
                )
    except FileNotFoundError:
        error_label = tk.Label(
            table_frame,
            text="Error: books.csv not found.",
            font=("Arial", 12),
            fg="red",
            bg="#f2f2f2"
        )
        error_label.pack()

    # Add a "Close" button
    close_button = tk.Button(
        view_books_window,
        text="Close",
        font=("Arial", 14, "bold"),
        bg="#4b0082",
        fg="white",
        command=view_books_window.destroy
    )
    close_button.pack(pady=10)

    view_books_window.mainloop()