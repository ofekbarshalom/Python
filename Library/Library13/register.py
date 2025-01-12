import tkinter as tk
from components.RoundedButton import RoundedButton
from User import *
from FileHandler import *
from utils import utils
from logger import Logger
from Users_dict import *
from NotificationSystem import NotificationSystem

log = Logger.get_logger()  # Get the logger instance

# Schedule window destruction and opening of the library
def proceed(current_window):
    from login import open_login_window  # Delayed import
    current_window.destroy()  # Destroy the current window
    open_login_window()  # Open the login interface

def add_user_to_notification_system(user):
    library_system = NotificationSystem.get_instance()
    library_system.add_observer(user)


@Logger.log_decorator("registered successfully", "registered fail")
def submit_register(name_entry, password_entry, current_window):
    name = name_entry.get()
    password = password_entry.get()

    if not name or not password:
        alert_label = tk.Label(current_window, text="Name and Password are required!", fg="red", font=("Arial", 12))
        alert_label.pack(pady=(10, 5))
        raise ValueError("Name or password missing")

    if FileHandler.check_name(name):
        alert_label = tk.Label(current_window, text="Name already exists!", fg="red", font=("Arial", 12))
        alert_label.pack(pady=(10, 5))
        raise ValueError("Name already exists")

    new_user = User(name, password)

    add_user_to_dict(new_user)

    add_user_to_notification_system(new_user)
    print(f"Librarian {new_user.name} created!")

    # Pass the current window to the proceed function
    current_window.after(100, lambda: proceed(current_window))


def open_register_window():
    # Main window setup
    register = tk.Tk()
    utils.center_window(register, 500, 400)
    register.title("Library/Register")
    register.configure(bg="#f2f2f2")  # Light gray background

    # Header
    header = tk.Label(register, text="Register", font=("Arial", 24, "bold"), bg="#4b0082", fg="white")
    header.pack(fill=tk.X, pady=(0, 20))  # Purple header

    # Frame for the form
    form_frame = tk.Frame(register, bg="#f2f2f2")
    form_frame.pack(pady=(20, 0))  # Move the form higher

    # Username Label and Entry
    username_label = tk.Label(form_frame, text="Username:", font=("Arial", 16), bg="#f2f2f2", fg="#4b0082")
    username_label.pack(anchor="w", pady=(5, 0))
    username_entry = tk.Entry(form_frame, font=("Arial", 14), width=30)
    username_entry.pack(pady=(0, 10))

    # Password Label and Entry
    password_label = tk.Label(form_frame, text="Password:", font=("Arial", 16), bg="#f2f2f2", fg="#4b0082")
    password_label.pack(anchor="w", pady=(5, 0))
    password_entry = tk.Entry(form_frame, font=("Arial", 14), show="*", width=30)
    password_entry.pack(pady=(0, 20))

    # Submit Button (Regular rectangular button)
    submit_button = tk.Button(
        form_frame,
        text="Submit",
        font=("Arial", 14, "bold"),
        bg="#4b0082",
        fg="white",
        width=20,
        command=lambda: submit_register(username_entry, password_entry, register),
    )
    submit_button.pack(pady=(10, 20))

    # Start Tkinter loop
    register.mainloop()

