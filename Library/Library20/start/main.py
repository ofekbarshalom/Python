from helpers.FileHandler import FileHandler
import pandas as pd
from design.NotificationSystem import NotificationSystem
from design.User import User
from helpers.path import Paths

def initialize_copies_available(books_df):
    if "is_loaned" not in books_df.columns or "copies" not in books_df.columns:
        raise ValueError("The DataFrame must contain 'is_loaned' and 'copies' columns.")

    # Check if 'copies_available' column already exists
    if "copies_available" not in books_df.columns:
        # Initialize the copies_available column
        books_df["copies_available"] = books_df.apply(
            lambda row: 0 if row["is_loaned"].strip().lower() == "yes" else row["copies"], axis=1
        )
        print("Initialized 'copies_available' column.")
    else:
        print("'copies_available' column already exists. Skipping initialization.")

    return books_df


def initialize_waiting_list(books_df):
    # Check if 'waiting_list' column already exists
    if "waiting_list" not in books_df.columns:
        # Add a new 'waiting_list' column, initialized with empty Queue objects
        books_df["waiting_list"] = "empty"
        print("Initialized 'waiting_list' column with empty strings.")
    else:
        print("'waiting_list' column already exists. Skipping initialization.")

    return books_df

def initialize_loaned_count(books_df):
    # Check if 'loaned_count' column already exists
    if "loaned_count" not in books_df.columns:
        # Add a new 'loaned_count' column, initialized to 0
        books_df["loaned_count"] = 0
        print("Initialized 'loaned_count' column with all values set to 0.")
    else:
        print("'loaned_count' column already exists. Skipping initialization.")

    return books_df

def initialize_users_messages(users_df):
    if "messages" not in users_df.columns:
        # Add a new 'messages' column, initialized to "empty"
        users_df["messages"] = "empty"
        print("Initialized 'messages' column with empty strings.")
    else:
        print("'messages' column already exists. Skipping initialization.")

    # Save the updated DataFrame back to the CSV to persist changes
    users_df.to_csv(Paths.USERS.value, index=False)
    return users_df


def get_users():
    # Load the users.csv file into a DataFrame
    users_df = pd.read_csv(Paths.USERS.value)
    # Convert the DataFrame to a list of User objects
    users_list = []
    for _, row in users_df.iterrows():
        user = User(row["name"], row["password"])
        # Set messages manually (as it's not set by the constructor)
        users_list.append(user)

    return users_list

def init_notification_system():
    notification_system = NotificationSystem.get_instance()
    # Get the list of users as User objects
    users = get_users()

    # Add each user to the notification system as an observer
    for user in users:
        notification_system.add_observer(user)
        print(f"User '{user.name}' added to the notification system.")

def main():
    # Load dataframes
    books_df, available_books_df, loaned_books_df = FileHandler.read_csv_files()
    # Initialize and save updated books_df
    books_df = initialize_copies_available(books_df)
    books_df = initialize_waiting_list(books_df)
    books_df = initialize_loaned_count(books_df)

    users_df = FileHandler.read_users_file()
    initialize_users_messages(users_df)

    init_notification_system()

    books_df.to_csv(Paths.BOOKS.value, index=False)  # Save changes back to CSV
    users_file_header = ["name", "password"]
    # Create the CSV file if it doesn't exist
    FileHandler.create_csv(Paths.USERS.value, users_file_header)

    popular_books_file_header = ["title", "requests"]
    # Create the CSV file if it doesn't exist
    FileHandler.create_csv(Paths.POPULAR_BOOKS.value, popular_books_file_header)

    FileHandler.init_loaned_books()
    FileHandler.init_available_books()
    FileHandler.init_logs()


if __name__ == "__main__":
    main()
