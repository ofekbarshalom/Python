import tkinter as tk
import hashlib

class utils:
    def center_window(self, width, height):
        # Get the screen's width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set the window's geometry to center it
        self.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def get_name_popup(text):
        # Create a temporary window
        popup = tk.Toplevel()
        utils.center_window(popup, 300, 200)
        popup.title("Enter Name")
        popup.resizable(False, False)

        # Variable to store the name
        name_var = tk.StringVar()

        # Widgets in the popup
        tk.Label(popup, text=text, font=("Arial", 12)).pack(pady=10)
        tk.Label(popup, text="Enter your name:", font=("Arial", 10)).pack(pady=5)
        name_entry = tk.Entry(popup, textvariable=name_var, font=("Arial", 10), width=30)
        name_entry.pack(pady=5)

        # Close the popup and set the name
        def submit_name():
            popup.destroy()  # Close the popup

        def cancel_popup():
            name_var.set("")  # Set name_var to empty string if canceled
            popup.destroy()

        # Frame to hold the buttons
        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)

        # Submit and Cancel buttons placed side by side
        tk.Button(button_frame, text="Submit", font=("Arial", 10), command=submit_name).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cancel", font=("Arial", 10), command=cancel_popup).pack(side="left", padx=5)

        # Wait for the popup to close
        popup.grab_set()
        popup.wait_window()

        # Return the entered name or None if empty
        return name_var.get() if name_var.get().strip() else None

    @staticmethod
    def notification_popup(messages):
        # Create the popup window
        popup = tk.Toplevel()
        Utils.center_window(popup, 400, 300)
        popup.title("Notifications")
        popup.resizable(False, False)

        # Create a frame to hold the scrollbar and listbox
        frame = tk.Frame(popup, bg="#f2f2f2")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox to display messages
        listbox = tk.Listbox(frame, font=("Arial", 12), yscrollcommand=scrollbar.set, width=50, height=15)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Attach the scrollbar to the listbox
        scrollbar.config(command=listbox.yview)

        # Add the messages to the listbox
        for message in messages:
            listbox.insert(tk.END, message)

        # Add a Close button
        close_button = tk.Button(
            popup,
            text="Close",
            font=("Arial", 12),
            bg="#4b0082",
            fg="white",
            command=popup.destroy
        )
        close_button.pack(pady=10)

        # Grab the focus for the popup
        popup.grab_set()
        popup.wait_window()

    @staticmethod
    def hash_password(password):
        # Create an SHA-256 hash object
        hash_object = hashlib.sha256()

        # Encode the password to bytes, then hash it
        hash_object.update(password.encode('utf-8'))

        # Get the hexadecimal representation of the hash
        return hash_object.hexdigest()