import tkinter as tk
from design.User import *
from helpers.FileHandler import FileHandler
from helpers.utils import utils
from helpers.logger import Logger
from design.NotificationSystem import NotificationSystem

log = Logger.get_logger()  # Get the logger instance

@Logger.log_decorator("registered successfully", "registered fail")
def submit_register(name_entry, password_entry, current_window, alert_label):
    """
        Handle user registration and add them as an observer.
    """
    name = name_entry.get()
    password = password_entry.get()

    # Check if name or password is missing
    if not name or not password:
        alert_label.config(text="Name and Password are required!", fg="red")
        current_window.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds

        raise ValueError("Registration failed: Name and Password are required.")

    # Check if the name already exists
    if FileHandler.check_name(name):
        alert_label.config(text="Name already exists!", fg="red")
        current_window.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds

        raise ValueError(f"Registration failed: Name '{name}' already exists!")

    # Create a new Librarian
    new_user = User(name, password)

    # add user to observers list
    notification_system = NotificationSystem.get_instance()
    notification_system.add_observer(new_user)

    print(f"User {new_user.name} created!")

    # Schedule window destruction and opening of the library
    def proceed():
        # Close the current window and open the login interface
        from buttons.login import open_login_window  # Delayed import
        current_window.destroy()
        open_login_window()

    current_window.after(100, proceed)  # Destroy and proceed after 100ms


def open_register_window():
    """
        Open the registration window.
    """
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

    # Inline Alert Label
    alert_label = tk.Label(register, text="", font=("Arial", 12), bg="#f2f2f2", fg="red")
    alert_label.pack(pady=(10, 5))

    # Submit Button (Regular rectangular button)
    submit_button = tk.Button(
        form_frame,
        text="Submit",
        font=("Arial", 14, "bold"),
        bg="#4b0082",
        fg="white",
        width=20,
        command=lambda: submit_register(username_entry, password_entry, register, alert_label),
    )
    submit_button.pack(pady=(10, 20))

    # Start Tkinter loop
    register.mainloop()
