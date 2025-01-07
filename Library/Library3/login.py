import tkinter as tk
from components.RoundedButton import RoundedButton
from register import open_register_window
from Librarian import *


def center_window(window, width, height):
    # Get the screen's width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window's geometry to center it
    window.geometry(f"{width}x{height}+{x}+{y}")

    # go to Register screen
def on_button_click(current_window):
    current_window.destroy()  # Close the current window
    open_register_window()    # Open the register window

    # check the login and Enter Library
def submit_login(username_entry, password_entry, current_window):
    from library import open_library_window

    # Get the input values from the entry fields
    name = username_entry.get()
    password = password_entry.get()

    if FileHandler.check_login(name, password):
        current_window.destroy()  # Close the current window
        open_library_window()  # Open the library interface
    else:
        # Display an alert message on the same window
        alert_label = tk.Label(current_window, text="Invalid username or password!", fg="red", font=("Arial", 12))
        alert_label.pack(pady=(10, 5))

        current_window.after(2000, alert_label.destroy)

def open_login_window():
    # Import `open_library_window` locally to avoid circular imports
    from library import open_library_window

    # Main window setup
    login = tk.Tk()
    center_window(login, 500, 550)
    login.title("Library/Login")
    login.configure(bg="#f2f2f2")  # Light gray background

    # Header (Placed at the top of the window)
    header = tk.Label(login, text="Login", font=("Arial", 24, "bold"), bg="#4b0082", fg="white")
    header.pack(fill=tk.X, pady=(0, 20))  # Purple header

    # Frame to center the form, moved higher up
    form_frame = tk.Frame(login, bg="#f2f2f2")
    form_frame.pack(pady=(20, 0))  # Reduced vertical padding to move the section upward

    # Username Label and Entry
    username_label = tk.Label(form_frame, text="Username:", font=("Arial", 18), bg="#f2f2f2", fg="#4b0082")
    username_label.pack(anchor="w", pady=(5, 0))  # Label placed above the input
    username_entry = tk.Entry(form_frame, font=("Arial", 18), width=30)
    username_entry.pack(pady=(0, 10))

    # Password Label and Entry
    password_label = tk.Label(form_frame, text="Password:", font=("Arial", 18), bg="#f2f2f2", fg="#4b0082")
    password_label.pack(anchor="w", pady=(5, 0))
    password_entry = tk.Entry(form_frame, font=("Arial", 18), show="*", width=30)
    password_entry.pack(pady=(0, 20))

    # Submit Button (Regular rectangular button)
    submit_button = tk.Button(
        form_frame,
        text="Submit",
        font=("Arial", 14, "bold"),
        bg="#4b0082",
        fg="white",
        width=20,
        command=lambda: submit_login(username_entry, password_entry, login),
    )
    submit_button.pack(pady=(0, 20))

    # Doesn't have a user? Text
    register_text = tk.Label(form_frame, text="Don't have an account?", font=("Arial", 14), bg="#f2f2f2", fg="#4b0082")
    register_text.pack(pady=(50, 5))

    # Register Button (Regular rectangular button)
    register_button = tk.Button(
        form_frame,
        text="Register",
        font=("Arial", 14, "bold"),
        bg="#4b0082",
        fg="white",
        width=20,
        command=lambda: on_button_click(login),
    )
    register_button.pack(pady=(10, 20))

    # Start the Tkinter loop
    login.mainloop()
