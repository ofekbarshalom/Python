import tkinter as tk
from components.RoundedButton import RoundedButton
from Librarian import *
from FileHandler import *


def center_window(window, width, height):
    # Get the screen's width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window's geometry to center it
    window.geometry(f"{width}x{height}+{x}+{y}")

def submit_register(name_entry, password_entry, current_window):
    name = name_entry.get()
    password = password_entry.get()

    if not name or not password:
        alert_label = tk.Label(current_window, text="Name and Password are required!", fg="red", font=("Arial", 12))
        alert_label.pack(pady=(10, 5))

        # Remove the alert after 2 seconds
        def safe_destroy():
            if alert_label.winfo_exists():  # Check if the widget exists
                alert_label.destroy()

        current_window.after(2000, safe_destroy)
        return

    if FileHandler.check_name(name):
        alert_label = tk.Label(current_window, text="Name already exist!", fg="red", font=("Arial", 12))
        alert_label.pack(pady=(10, 5))
        return

    # Create a new Librarian
    new_librarian = Librarian(name, password)
    print(f"Librarian {new_librarian.name} created!")

    # Close the current window and open the library interface
    from login import open_login_window  # Delayed import
    current_window.destroy()
    open_login_window()

def open_register_window():
    # Main window setup
    register = tk.Tk()
    center_window(register, 500, 400)
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

