import tkinter as tk
import pandas as pd
from helpers.FileHandler import FileHandler
from helpers.path import Paths
from design.NotificationSystem import NotificationSystem


class utils:
    """
        A utility class with static methods for managing UI, book data, and notifications in the library system.
    """
    def center_window(self, width, height):
        """
            Centers a Tkinter window on the screen.
            :param width: Width of the window.
            :param height: Height of the window.
        """
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
        """
            Loads book data into a Treeview widget.
            :param tree: Tkinter Treeview widget.
            :param books_df: DataFrame containing book data.
        """
        # Clear existing data in the Treeview
        for item in tree.get_children():
            tree.delete(item)
        # Insert new data
        for _, row in books_df.iterrows():
            tree.insert("", tk.END, values=list(row))

    @staticmethod
    def calculate_waiting_list_size(waiting_list_str):
        """
            Calculates the size of a waiting list from a string.
            :param waiting_list_str: Comma-separated string of names or "empty".
            :return: Number of names in the waiting list.
        """
        if waiting_list_str != "empty":
            request_count = len(waiting_list_str.split(","))
        else:
            request_count = 0

        return request_count

    @staticmethod
    def get_name_popup(text):
        """
            Displays a popup window to capture the user's name.
            :param text: Instructional text displayed in the popup.
            :return: The entered name or None if canceled.
        """
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
        """
            Adds a client to a book's waiting list and updates the CSV file.
            :param book_title: Title of the book.
            :param client_name: Name of the client.
            :param books_df: DataFrame containing book data.
            :param file_path: Path to the CSV file.
        """
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

        request_count = utils.calculate_waiting_list_size(waiting_list_str)

        utils.check_and_update_book_in_popular_books(book_title, request_count + loaned_count)

        # Print confirmation message
        print(f"Client '{client_name}' added to the waiting list of book '{book_title}'.")
        return True

    @staticmethod
    def get_book_with_lowest_requests_and_loans(popular_books_df):
        """
            Finds the book with the lowest number of requests and loans in the popular books DataFrame.
            :param popular_books_df: DataFrame containing popular books and their request counts.
            :return: Tuple of the book title and its request count, or None if the DataFrame is empty.
        """
        if popular_books_df.empty:
            print("The popular_books DataFrame is empty.")
            return None

        # Find the row with the minimum requests value
        min_row = popular_books_df.loc[popular_books_df["requests"].idxmin()]

        # Return the book title and the requests count
        return min_row["title"], min_row["requests"]

    @staticmethod
    def update_book_in_popular_books(book_title, popular_books_df, book_request_and_loaned_count):
        """
            Updates or adds a book in the popular books DataFrame based on its request and loan count.
            Removes the book if its request count is zero.
            :param book_title: Title of the book.
            :param popular_books_df: DataFrame of popular books.
            :param book_request_and_loaned_count: Combined count of requests and loans for the book.
        """
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
        """
            Checks and updates the popular books list based on the given book's request and loan count.
            Ensures the list has a maximum of 10 entries, prioritizing books with higher counts.
            :param book_title: Title of the book.
            :param book_request_and_loaned_count: Combined count of requests and loans for the book.
        """
        # Load the popular_books.csv file into a DataFrame
        popular_books_df = FileHandler.read_popular_books_file()

        row_count = popular_books_df.shape[0]
        if row_count >= 10:
            lowest_count_book_title, lowest_count_book_total = utils.get_book_with_lowest_requests_and_loans(popular_books_df)

            if lowest_count_book_total < book_request_and_loaned_count:
                update_book_in_popular_books(book_title, popular_books_df, book_request_and_loaned_count)
        else:
            utils.update_book_in_popular_books(book_title, popular_books_df, book_request_and_loaned_count)

    @staticmethod
    def add_message_to_users(message):
        """
            Notify all users (observers) at the message
        """

        users_df = FileHandler.read_users_file()
        notification_system = NotificationSystem.get_instance()
        notification_system.notify_observers(message, users_df)
