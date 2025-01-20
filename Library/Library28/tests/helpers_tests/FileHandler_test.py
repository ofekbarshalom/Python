import unittest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
from helpers.FileHandler import FileHandler
from helpers.path import Paths
import hashlib

class TestFileHandler(unittest.TestCase):
    # ----------------------------------------
    # Test for create_csv
    # ----------------------------------------
    @patch("helpers.FileHandler.pd.read_csv")
    @patch("helpers.FileHandler.pd.DataFrame.to_csv")
    def test_create_csv_new_file(self, mock_to_csv, mock_read_csv):
        # Mock FileNotFoundError for read_csv
        mock_read_csv.side_effect = FileNotFoundError

        # Call the method
        FileHandler.create_csv("test.csv", headers=["title", "author", "year"])

        # Verify that the file was created with headers
        mock_to_csv.assert_called_once_with("test.csv", index=False)

    @patch("helpers.FileHandler.pd.read_csv")
    def test_create_csv_existing_file(self, mock_read_csv):
        # Mock successful read_csv
        mock_read_csv.return_value = pd.DataFrame(columns=["title", "author", "year"])

        # Call the method
        FileHandler.create_csv("test.csv", headers=["title", "author", "year"])

        # Ensure that no file creation occurs
        mock_read_csv.assert_called_once_with("test.csv")

    # ----------------------------------------
    # Test for init_available_books
    # (The logic for init_popular_books and init_loaned_books is similar, so separate tests are unnecessary)
    # ----------------------------------------
    @patch("helpers.FileHandler.pd.read_csv")
    @patch("helpers.FileHandler.pd.DataFrame.to_csv")
    def test_init_available_books(self, mock_to_csv, mock_read_csv):
        # Mock the content of available_books.csv
        mock_read_csv.side_effect = [
            pd.DataFrame({
                "title": ["Book A"],
                "copies_available": [1]
            }),  # available_books.csv already exists
            pd.DataFrame({
                "title": ["Book A", "Book B"],
                "copies_available": [1, 0],
            })  # books.csv
        ]

        # Call the method
        FileHandler.init_available_books()

        # Verify that initialization was skipped (no file creation)
        mock_to_csv.assert_not_called()
        print("Initialization skipped as available_books.csv already exists.")

    # ----------------------------------------
    # Test for init_logs
    # ----------------------------------------
    @patch("builtins.open", new_callable=mock_open)
    def test_init_logs_file_exists(self, mock_open_fn):
        # Mock the file open operation to simulate the file already existing
        mock_open_fn.return_value.__enter__.return_value = MagicMock()

        # Call the method
        FileHandler.init_logs(log_file_path="mock_log_file.log")

        # Verify that the file was opened in read mode
        mock_open_fn.assert_called_once_with("mock_log_file.log", "r")
        print("Log file already exists. Initialization skipped.")

    # ----------------------------------------
    # Test for check_login
    # ----------------------------------------
    @patch("helpers.FileHandler.FileHandler.read_users_file")
    def test_check_login(self, mock_read_users_file):
        # Mock the users DataFrame
        mock_read_users_file.return_value = pd.DataFrame({
            "name": ["ofek"],
            "password": [FileHandler.hash_password("password123")]
        })

        # Test with valid credentials
        result_valid = FileHandler.check_login("ofek", "password123")
        self.assertTrue(result_valid, "Expected login to succeed with valid credentials")

        # Test with incorrect username
        result_invalid_username = FileHandler.check_login("wrongusername", "password123")
        self.assertFalse(result_invalid_username, "Expected login to fail with an incorrect username")

        # Test with incorrect password
        result_invalid_password = FileHandler.check_login("ofek", "wrongpassword")
        self.assertFalse(result_invalid_password, "Expected login to fail with an incorrect password")

        # Test with both incorrect username and password
        result_invalid_both = FileHandler.check_login("wrongusername", "wrongpassword")
        self.assertFalse(result_invalid_both, "Expected login to fail with both username and password incorrect")

    # ----------------------------------------
    # Test for hash_password
    # ----------------------------------------
    def test_hash_password(self):
        # Input plaintext password
        password = "securepassword"

        # Expected hash using hashlib directly
        expected_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Call the method
        result = FileHandler.hash_password(password)

        # Assertions
        self.assertEqual(result, expected_hash, "The hashed password does not match the expected hash")

    # ----------------------------------------
    # Test for check_name
    # ----------------------------------------
    @patch("helpers.FileHandler.FileHandler.read_users_file")
    def test_check_name(self, mock_read_users_file):
        # Mock the users DataFrame
        mock_read_users_file.return_value = pd.DataFrame({
            "name": ["ofek", "roy", "naama"]
        })

        # Test with a username that exists
        self.assertTrue(
            FileHandler.check_name("ofek"),
            "Expected check_name to return True for an existing username"
        )

        # Test with a username that does not exist
        self.assertFalse(
            FileHandler.check_name("dror"),
            "Expected check_name to return False for a non-existing username"
        )

    # ----------------------------------------
    # Test for read_user_files
    # (read_csv_files and read_popular_books_file are the same logic, so they don't have a test)
    # ----------------------------------------
    @patch("helpers.FileHandler.pd.read_csv")
    def test_read_users_file_file_exists(self, mock_read_csv):
        # Mock the DataFrame returned by pd.read_csv
        mock_read_csv.return_value = pd.DataFrame({
            "name": ["Alice", "Bob"],
            "password": ["hashed_password_1", "hashed_password_2"],
            "messages": ["Message 1", "Message 2"]
        })

        # Call the method
        result = FileHandler.read_users_file()

        # Assertions
        mock_read_csv.assert_called_once_with(Paths.USERS.value)  # Ensure correct file is read
        self.assertEqual(len(result), 2, "Expected two rows in the DataFrame")
        self.assertIn("name", result.columns, "Expected 'name' column in the DataFrame")
        self.assertIn("password", result.columns, "Expected 'password' column in the DataFrame")
        self.assertIn("messages", result.columns, "Expected 'messages' column in the DataFrame")

    @patch("helpers.FileHandler.pd.read_csv")
    def test_read_users_file_file_not_found(self, mock_read_csv):
        # Mock FileNotFoundError for pd.read_csv
        mock_read_csv.side_effect = FileNotFoundError

        # Call the method
        result = FileHandler.read_users_file()

        # Assertions
        mock_read_csv.assert_called_once_with(Paths.USERS.value)  # Ensure correct file is read
        self.assertTrue(result.empty, "Expected an empty DataFrame when file is not found")
        self.assertListEqual(
            list(result.columns), ["name", "password", "messages"],
            "Expected DataFrame to have 'name', 'password', and 'messages' columns"
        )
