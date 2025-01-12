import tkinter as tk
from components.RoundedButton import RoundedButton
from register import open_register_window
from User import *
from utils import utils
from logger import Logger

log = Logger.get_logger()  # Get the logger instance


# go to Register screen
def on_button_click(current_window):
    current_window.destroy()  # Close the current window
    open_register_window()    # Open the register window


# check the login and Enter Library
@Logger.log_decorator("logged in successfully", "Logged in fail")
def submit_login(username_entry, password_entry, current_window):
    from library import open_library_window

    name = username_entry.get()
    password = password_entry.get()

    if FileHandler.check_login(name, password):
        # Schedule window destruction and opening of the library
        def proceed():
            current_window.destroy()
            utils.show_messages_pop_up(name)
            open_library_window()

        current_window.after(100, proceed)  # Destroy and proceed after 100ms
    else:
        alert_label = tk.Label(current_window, text="Invalid username or password!", fg="red", font=("Arial", 12))
        alert_label.pack(pady=(10, 5))
        current_window.after(2000, alert_label.destroy)
        raise ValueError("Invalid username or password")  # Trigger the failure log

def open_login_window():
    # Import `open_library_window` locally to avoid circular imports
    from library import open_library_window

    # Main window setup
    login = tk.Tk()
    utils.center_window(login, 500, 550)
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
