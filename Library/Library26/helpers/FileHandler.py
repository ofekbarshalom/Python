import hashlib
from helpers.path import Paths
import pandas as pd

class FileHandler:
    """
        Utility class for handling file operations in the library system.
    """
    @staticmethod
    def create_csv(file_path, headers=None):
        """
            Create a CSV file with the specified headers if it doesn't exist.
            :param file_path: Path to the CSV file.
            :param headers: List of column headers for the CSV.
        """
        if headers is None or not isinstance(headers, list):
            raise ValueError("Headers must be provided as a list of column names.")

        try:
            # Attempt to read the CSV file to check if headers already exist
            existing_data = pd.read_csv(file_path)
            print(f"'{file_path}' already exist.")
        except FileNotFoundError:
            # If the file doesn't exist, create it with the specified headers
            pd.DataFrame(columns=headers).to_csv(file_path, index=False)
            print(f"Headers added to '{file_path}': {headers}")
        except pd.errors.EmptyDataError:
            # If the file exists but is empty, add headers
            pd.DataFrame(columns=headers).to_csv(file_path, index=False)
            print(f"Headers added to '{file_path}': {headers}")

    @staticmethod
    def init_available_books(books_file_path=Paths.BOOKS.value, available_books_file_path=Paths.AVAILABLE_BOOKS.value):
        """
            Initialize the available_books.csv file with books having available copies.
        """
        # Check if the available_books.csv file already exists
        try:
            pd.read_csv(available_books_file_path)
            print(f"The file '{available_books_file_path}' already exists. Initialization skipped.")
            return  # If the file exists, do nothing
        except FileNotFoundError:
            pass  # Proceed if the file does not exist

        # Try to load the books.csv file
        try:
            # Load books.csv into a DataFrame
            books_df = pd.read_csv(books_file_path)
        except FileNotFoundError:
            print(f"The file '{books_file_path}' does not exist.")
            return

        # Filter rows where 'copies_available' is greater than 0
        filtered_books = books_df[books_df['copies_available'] > 0]

        # Select only the 'title' and 'copies_available' columns
        available_books_df = filtered_books[['title', 'copies_available']]

        # Save the filtered DataFrame to available_books.csv
        available_books_df.to_csv(available_books_file_path, index=False)

        print(f"The file '{available_books_file_path}' has been successfully updated with available books.")

    @staticmethod
    def init_loaned_books(books_file_path=Paths.BOOKS.value, loaned_books_file_path=Paths.LOANED_BOOKS.value):
        """
            Initialize the loaned_books.csv file with books currently loaned out.
        """
        # Check if the loaned_books.csv file already exists
        try:
            pd.read_csv(loaned_books_file_path)
            print(f"The file '{loaned_books_file_path}' already exists. Initialization skipped.")
            return  # If the file exists, do nothing
        except FileNotFoundError:
            pass  # Proceed if the file does not exist

        # Try to load the books.csv file
        try:
            # Load books.csv into a DataFrame
            books_df = pd.read_csv(books_file_path)
        except FileNotFoundError:
            print(f"The file '{books_file_path}' does not exist.")
            return

        # Filter rows where 'is_loaned' is "Yes"
        loaned_books_df = books_df[books_df['is_loaned'] == "Yes"]

        # Select only the 'title' column
        loaned_books_df = loaned_books_df[['title']]

        # Save the filtered DataFrame to loaned_books.csv
        loaned_books_df.to_csv(loaned_books_file_path, index=False)

        print(f"The file '{loaned_books_file_path}' has been successfully updated with loaned books.")

    @staticmethod
    def init_logs(log_file_path=Paths.LOGGER.value):
        """
            Initialize the log file if it doesn't exist.
        """
        try:
            # Try to open the file in read mode
            with open(log_file_path, 'r') as log_file:
                print(f"The log file '{log_file_path}' already exists. Initialization skipped.")
                return  # File exists, so do nothing
        except FileNotFoundError:
            # If the file does not exist, create it
            with open(log_file_path, 'w') as log_file:
                log_file.write("")  # Create an empty file
            print(f"The log file '{log_file_path}' has been created successfully.")

    @staticmethod
    def check_login(name, password):
        """
            Validate user login credentials.
            :param name: The username.
            :param password: The plaintext password.
            :return: True if credentials are valid, otherwise False.
        """
        # Use read_users_file to get the users DataFrame
        df = FileHandler.read_users_file()

        # Check if the username exists in the DataFrame
        user_row = df[df["name"] == name]

        if not user_row.empty:
            # Hash the provided password
            hashed_password = FileHandler.hash_password(password)

            # Check if the hashed password matches
            if user_row.iloc[0]["password"] == hashed_password:
                return True  # Username and password are correct
            else:
                print("Password is incorrect")
                return False  # Incorrect password
        else:
            print("Username is incorrect")
            return False  # Username not found

    @staticmethod
    def hash_password(password):
        """
            Hash a plaintext password using SHA-256.
            :param password: The plaintext password.
            :return: The hashed password as a hexadecimal string.
        """
        # Create an SHA-256 hash object
        hash_object = hashlib.sha256()

        # Encode the password to bytes, then hash it
        hash_object.update(password.encode('utf-8'))

        # Get the hexadecimal representation of the hash
        return hash_object.hexdigest()

    @staticmethod
    def check_name(name):
        """
            Check if a username exists in users.csv.
            :param name: The username to check.
            :return: True if the username exists, otherwise False.
        """
        # Use read_users_file to get the users DataFrame
        user_df = FileHandler.read_users_file()

        # Check if the username exists in the DataFrame
        if name in user_df["name"].values:
            return True  # Username found
        else:
            return False  # Username not found

    @staticmethod
    def read_csv_files():
        """
            Read and return DataFrames for books, available_books, and loaned_books.
            :return: Tuple of DataFrames (books_df, available_books_df, loaned_books_df).
        """
        # Try to read books.csv
        try:
            books_df = pd.read_csv(Paths.BOOKS.value)
            print("books.csv loaded successfully.")
        except FileNotFoundError:
            books_df = pd.DataFrame(columns=["title", "copies", "copies_available", "is_loaned"])
            print("books.csv does not exist. Returning an empty DataFrame.")

        # Try to read available_books.csv
        try:
            available_books_df = pd.read_csv(Paths.AVAILABLE_BOOKS.value)
            print("available_books.csv loaded successfully.")
        except FileNotFoundError:
            available_books_df = pd.DataFrame(columns=["title", "copies_available"])
            print("available_books.csv does not exist. Returning an empty DataFrame.")

        # Try to read loaned_books.csv
        try:
            loaned_books_df = pd.read_csv(Paths.LOANED_BOOKS.value)
            print("loaned_books.csv loaded successfully.")
        except FileNotFoundError:
            loaned_books_df = pd.DataFrame(columns=["title"])
            print("loaned_books.csv does not exist. Returning an empty DataFrame.")

        return books_df, available_books_df, loaned_books_df

    @staticmethod
    def read_popular_books_file():
        """
            Read and return the popular_books.csv file.
            :return: DataFrame of popular books.
        """
        # Try to read popular_books.csv
        try:
            popular_books_df = pd.read_csv(Paths.POPULAR_BOOKS.value)
            print("popular_books.csv loaded successfully.")
        except FileNotFoundError:
            popular_books_df = pd.DataFrame(columns=["title"])
            print("popular_books.csv does not exist. Returning an empty DataFrame.")

        return popular_books_df

    @staticmethod
    def read_users_file():
        """
            Read and return the users.csv file.
            :return: DataFrame of users.
        """
        # Try to read users.csv
        try:
            users_df = pd.read_csv(Paths.USERS.value)
            print("users.csv loaded successfully.")
        except FileNotFoundError:
            # Create an empty DataFrame with the appropriate columns
            users_df = pd.DataFrame(columns=["name", "password", "messages"])
            print("users.csv does not exist. Returning an empty DataFrame.")

        return users_df
