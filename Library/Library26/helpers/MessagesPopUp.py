import tkinter as tk
from tkinter import ttk, messagebox
from helpers.FileHandler import FileHandler
from helpers.path import Paths
from helpers.utils import utils


class MessagesPopUp:
    """
        A class to display a pop-up window showing user-specific messages.
    """
    @staticmethod
    def show_messages_pop_up(user_name):
        """
            Display a pop-up window with messages for the specified user.
            :param user_name: The name of the user whose messages are to be displayed.
        """
        users_df = FileHandler.read_users_file()

        # Find the user in the DataFrame
        user_row = users_df[users_df["name"] == user_name]

        # Ensure the user exists
        if user_row.empty:
            tk.messagebox.showerror("Error", f"User '{user_name}' not found.")
            return

        # Retrieve messages and handle "empty" case
        messages = user_row["messages"].values[0]
        if messages == "empty":
            messages = "No messages available."
        else:
            # Format messages to show each message on a new line
            messages = messages.replace(",", ".\n\n").strip()
            if not messages.endswith("."):
                messages += "."

        # Create the pop-up window
        pop_up = tk.Tk()
        utils.center_window(pop_up, 550, 400)
        pop_up.title(f"Messages for {user_name}")
        pop_up.configure(bg="#f2f2f2")

        # Header Label
        header = tk.Label(pop_up, text=f"Messages for {user_name}", font=("Arial", 16, "bold"), bg="#4b0082",
                          fg="white")
        header.pack(fill=tk.X, pady=(10, 10))

        # Create a frame for scrollable content
        frame = tk.Frame(pop_up, bg="#f2f2f2")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add a canvas to the frame
        canvas = tk.Canvas(frame, bg="#f2f2f2")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the frame
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas for the messages
        messages_frame = tk.Frame(canvas, bg="#f2f2f2")
        canvas.create_window((0, 0), window=messages_frame, anchor="nw")

        # Add the messages to the frame
        messages_label = tk.Label(
            messages_frame,
            text=messages,
            font=("Arial", 12),
            bg="#f2f2f2",
            justify="left",
            wraplength=550,
        )
        messages_label.pack(anchor="w", pady=5)

        # Close Button
        def on_close():
            # Clear messages for the user
            user_row_index = users_df[users_df["name"] == user_name].index[0]
            users_df.at[user_row_index, "messages"] = "empty"

            # Save changes to the CSV file
            users_df.to_csv(Paths.USERS.value, index=False)
            print(f"Messages for user '{user_name}' have been cleared.")

            # Close the pop-up
            pop_up.destroy()

        close_button = tk.Button(
            pop_up,
            text="Close",
            font=("Arial", 12, "bold"),
            bg="#4b0082",
            fg="white",
            command=on_close,
        )
        close_button.pack(pady=10)

        pop_up.mainloop()
