import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from FileHandler import FileHandler
from path import Paths
from Book import Book
from logger import Logger

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
    def load_books(tree, books_df):
        # Clear existing data in the Treeview
        for item in tree.get_children():
            tree.delete(item)
        # Insert new data
        for _, row in books_df.iterrows():
            tree.insert("", tk.END, values=list(row))

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
    def update_book_waiting_list(book_title, client_name, books_df, file_path):
        # Check if the book exists in books_df
        if book_title not in books_df["title"].values:
            print(f"Book '{book_title}' not found in the DataFrame.")
            return False

        # Get the row index for the specific book
        book_row_index = books_df.index[books_df["title"] == book_title][0]

        # Retrieve the current waiting_list string
        waiting_list_str = books_df.at[book_row_index, "waiting_list"]

        # Add the client to the waiting list string
        if waiting_list_str == "empty":  # If the waiting list is not empty
            waiting_list_str = client_name
        else:  # If the waiting list is empty, add the name directly
            waiting_list_str += f",{client_name}"

        # Update the waiting_list column
        books_df.at[book_row_index, "waiting_list"] = waiting_list_str

        # Retrieve the loaned_count for the book
        loaned_count = books_df.at[book_row_index, "loaned_count"]

        # Save the updated DataFrame back to the CSV
        books_df.to_csv(file_path, index=False)
        print(f"Changes saved to {file_path}.")

        # Calculate the total for popular books logic
        queue_length = len(waiting_list_str.split(","))  # Calculate number of names in the list
        utils.check_and_update_book_in_popular_books(book_title, queue_length + loaned_count)

        # Print confirmation message
        print(f"Client '{client_name}' added to the waiting list of book '{book_title}'.")
        return True

    @staticmethod
    def get_book_with_lowest_requests_and_loans(popular_books_df):
        if popular_books_df.empty:
            print("The popular_books DataFrame is empty.")
            return None

        # Find the row with the minimum requests value
        min_row = popular_books_df.loc[popular_books_df["requests"].idxmin()]

        # Return the book title and the requests count
        return min_row["title"], min_row["requests"]

    @staticmethod
    def update_book_in_popular_books(book_title, popular_books_df, book_request_and_loaned_count):
        # Check if the book exists in the DataFrame
        if book_title in popular_books_df["title"].values:
            # Update or remove the book based on the book_request value
            if book_request_and_loaned_count == 0:
                # Remove the book
                popular_books_df = popular_books_df[popular_books_df["title"] != book_title]
                print(f"Book '{book_title}' removed from popular_books.csv as request count is 0.")
            else:
                # Update the book_request value
                popular_books_df.loc[
                    popular_books_df["title"] == book_title, "requests"] = book_request_and_loaned_count
                print(f"Book '{book_title}' updated with request count {book_request_and_loaned_count}.")
        else:
            # Add the book if it doesn't exist
            if book_request_and_loaned_count > 0:
                new_row = {"title": book_title, "requests": book_request_and_loaned_count}
                popular_books_df = pd.concat([popular_books_df, pd.DataFrame([new_row])], ignore_index=True)
                print(
                    f"Book '{book_title}' added to popular_books.csv with request count {book_request_and_loaned_count}.")
            else:
                print(f"Book '{book_title}' not added as request count is 0.")

        # Save the updated DataFrame back to the CSV file
        popular_books_df.to_csv(Paths.POPULAR_BOOKS.value, index=False)

    @staticmethod
    def check_and_update_book_in_popular_books(book_title, book_request_and_loaned_count):
        # Load the popular_books.csv file into a DataFrame
        popular_books_df = FileHandler.read_popular_books_file()

        row_count = popular_books_df.shape[0]
        if row_count >= 10:
            lowest_count_book_title, lowest_count_book_total = utils.get_book_with_lowest_requests_and_loans(popular_books_df)

            if lowest_count_book_total < book_request_and_loaned_count:
                update_book_in_popular_books(book_title, popular_books_df, book_request_and_loaned_count)
        else:
            utils.update_book_in_popular_books(book_title, popular_books_df, book_request_and_loaned_count)
