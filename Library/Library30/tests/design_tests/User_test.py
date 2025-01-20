import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from design.User import User
from helpers.FileHandler import FileHandler
from helpers.path import Paths
from start.Book import Book


class TestUser(unittest.TestCase):
    # ----------------------------------------
    # Test for user_initialization
    # ----------------------------------------
    @patch("design.User.FileHandler.read_users_file")
    @patch("design.User.pd.DataFrame.to_csv")
    def test_user_initialization(self, mock_to_csv, mock_read_users_file):
        # Prepare mock data for read_users_file
        mock_read_users_file.return_value = pd.DataFrame(columns=["name", "password", "messages"])

        # Create a User object (this will call add_user_to_csv internally)
        user = User(name="testuser", password="securepassword123")

        # Assertions to ensure proper initialization
        self.assertEqual(user.name, "testuser")
        self.assertEqual(user.password, FileHandler.hash_password("securepassword123"))  # Check hashed password
        self.assertEqual(user.messages, [])

        # Assert that the user was added to the mocked DataFrame
        mock_to_csv.assert_called_once()  # Ensure to_csv is called once

    # ----------------------------------------
    # Test for add_user_to_csv
    # ----------------------------------------
    @patch("design.User.FileHandler.read_users_file")
    @patch("design.User.FileHandler.check_name")
    @patch("design.User.pd.DataFrame.to_csv")
    def test_add_user_to_csv(self, mock_to_csv, mock_check_name, mock_read_users_file):
        # Mock the users DataFrame
        mock_users_df = pd.DataFrame({
            "name": ["existing_user"],
            "password": ["hashed_password"],
            "messages": ["empty"]
        })
        mock_read_users_file.return_value = mock_users_df

        # Case 1: User already exists
        mock_check_name.return_value = True
        user = User(name="existing_user", password="hashed_password")
        user.add_user_to_csv()
        mock_to_csv.assert_not_called()  # Ensure no CSV write for existing user

        # Case 2: User does not exist
        mock_check_name.return_value = False
        user = User(name="new_user", password="hashed_password")
        user.add_user_to_csv()

        # Assert the new user is added and written to CSV
        mock_to_csv.assert_called_with(Paths.USERS.value, index=False)  # Ensure the DataFrame is saved

    # ----------------------------------------
    # Test for add_book_to_library
    # ----------------------------------------
    @patch("helpers.FileHandler.FileHandler.read_csv_files")
    @patch("helpers.FileHandler.pd.DataFrame.to_csv")
    def test_add_book_to_library(self, mock_to_csv, mock_read_csv_files):
        # Mock initial data
        mock_books_df = pd.DataFrame({
            "title": ["Book1"],
            "author": ["Author1"],
            "is_loaned": ["No"],
            "copies": [5],
            "genre": ["Fiction"],
            "year": [2020],
            "copies_available": [5],
            "waiting_list": ["empty"],
            "loaned_count": [0]
        })
        mock_available_books_df = pd.DataFrame({
            "title": ["Book1"],
            "copies_available": [5]
        })
        mock_read_csv_files.return_value = (mock_books_df, mock_available_books_df, None)

        # Create a mock Book object
        mock_book = Book(
            title="New Book",
            author="New Author",
            is_loaned="No",
            copies=10,
            genre="Science Fiction",
            year=2023
        )

        # Call the method to test
        User.add_book_to_library(mock_book)

        # Assertions
        # Check if the new book was added to books_df
        self.assertTrue(mock_books_df.equals(mock_read_csv_files.return_value[0]))
        mock_to_csv.assert_any_call(Paths.BOOKS.value, index=False)

        # Check if the new available book was added to available_books_df
        self.assertTrue(mock_available_books_df.equals(mock_read_csv_files.return_value[1]))
        mock_to_csv.assert_any_call(Paths.AVAILABLE_BOOKS.value, index=False)

    # ----------------------------------------
    # Test for update
    # ---------------------------------------
    @patch("design.User.FileHandler.read_users_file")
    @patch("design.User.pd.DataFrame.to_csv")
    def test_update_method(self, mock_to_csv, mock_read_users_file):
        # Mock initial user data
        mock_users_df = pd.DataFrame({
            "name": ["testuser", "otheruser"],
            "password": ["hashed_password1", "hashed_password2"],
            "messages": ["empty", "Hello"]
        })
        mock_read_users_file.return_value = mock_users_df

        # Create a User instance
        user = User(name="testuser", password="securepassword123")

        # Call the update method
        user.update("New message", mock_users_df)

        # Assert the message is updated in the user's messages list
        self.assertIn("New message", user.messages)

        # Assert the users DataFrame is updated correctly
        user_row_index = mock_users_df[mock_users_df["name"] == "testuser"].index[0]
        self.assertEqual(mock_users_df.at[user_row_index, "messages"], "New message")

        # Call the update method again with another message
        user.update("Another message", mock_users_df)

        # Assert the messages are concatenated
        self.assertEqual(mock_users_df.at[user_row_index, "messages"], "New message,Another message")


if __name__ == "__main__":
    unittest.main()
