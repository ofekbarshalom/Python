import tkinter as tk
from buttons.AddBook import open_add_new_book_window
from buttons.ViewBooks import open_view_books_window
from buttons.SearchBook import open_search_books_window
from buttons.RemoveBook import open_remove_book_window
from buttons.LendBook import open_lend_book_window
from buttons.ReturnBook import open_return_book_window
from buttons.PopularBooks import open_popular_books_window
from helpers.utils import utils
from helpers.logger import Logger

log = Logger.get_logger()  # Get the logger instance

@Logger.log_decorator("log out successfully", "log out fail")
def logout_and_go_to_landing(current_window):
    from Landing import open_landing_page

    # Schedule window destruction and opening of the library
    def proceed():
        current_window.destroy()
        open_landing_page()  # Open the landing page

    current_window.after(100, proceed)  # Destroy and proceed after 100ms

def go_to_login_screen(current_window):
    from buttons.login import open_login_window

    current_window.destroy()  # Close the current window
    open_login_window()  # Open the login screen

def go_to_register_screen(current_window):
    from buttons.register import open_register_window

    current_window.destroy()  # Close the current window
    open_register_window()  # Open the register screen

def open_library_window():
    # Main window setup
    root = tk.Tk()
    utils.center_window(root, 1000, 300)  # Smaller window since we only show buttons now
    root.title("Library")
    root.configure(bg="#f2f2f2")

    # Header
    header = tk.Label(root, text="Library", font=("Arial", 24, "bold"), bg="#4b0082", fg="white")
    header.pack(fill=tk.X, pady=(0, 10))

    # Buttons Frame
    buttons_frame = tk.Frame(root, bg="#f2f2f2")
    buttons_frame.pack(pady=(20, 20), expand=True)

    # Buttons Data with Actions
    buttons = [
        ("Add Book", lambda: open_add_new_book_window()),
        ("Remove Book", lambda: open_remove_book_window()),
        ("Search Book", lambda: open_search_books_window()),
        ("View Books", lambda: open_view_books_window()),
        ("Lend Book", lambda: open_lend_book_window()),
        ("Return Book", lambda: open_return_book_window()),
        ("Logout", lambda: logout_and_go_to_landing(root)),
        ("Login", lambda: go_to_login_screen(root)),
        ("Register", lambda: go_to_register_screen(root)),
        ("Popular Books", lambda: open_popular_books_window()),
    ]

    # Create buttons in rows and columns
    for idx, (label, action) in enumerate(buttons):
        row = idx // 5  # 5 buttons per row
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
