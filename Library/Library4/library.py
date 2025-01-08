import tkinter as tk
from AddBook import open_add_new_book_window
from ViewBooks import open_view_books_window
from SearchBook import open_search_books_window


def center_window(window, width, height):
    # Get the screen's width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window's geometry to center it
    window.geometry(f"{width}x{height}+{x}+{y}")


def dummy_command(action):
    print(f"{action} button clicked!")

def logout_and_go_to_landing(current_window):
    from Landing import open_landing_page

    current_window.destroy()  # Close the current library window
    open_landing_page()  # Open the landing page

def go_to_login_screen(current_window):
    from login import open_login_window

    current_window.destroy()  # Close the current window
    open_login_window()  # Open the login screen

def go_to_register_screen(current_window):
    from register import open_register_window

    current_window.destroy()  # Close the current window
    open_register_window()  # Open the register screen

def open_library_window():
    # Main window setup
    root = tk.Tk()
    center_window(root, 700, 400)  # Smaller window since we only show buttons now
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
        ("Remove Book", lambda: dummy_command("Remove Book")),
        ("View Books", lambda: open_view_books_window()),
        ("Search Book", lambda: open_search_books_window()),
        ("Return Book", lambda: dummy_command("Return Book")),
        ("Logout", lambda: logout_and_go_to_landing(root)),
        ("Login", lambda: go_to_login_screen(root)),
        ("Register", lambda: go_to_register_screen(root)),
        ("Popular Books", lambda: dummy_command("Popular Books")),
    ]

    # Create buttons in rows and columns
    for idx, (label, action) in enumerate(buttons):
        row = idx // 3  # 3 buttons per row
        col = idx % 3
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
