import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from start.main import *
from helpers.path import Paths

class TestMain(unittest.TestCase):
    # ----------------------------------------
    # Test initialize_copies_available
    # ----------------------------------------
    def test_initialize_copies_available(self):
        books_df = pd.DataFrame({
            "title": ["Book A", "Book B"],
            "is_loaned": ["Yes", "No"],
            "copies": [2, 5]
        })

        # Call the function
        updated_df = initialize_copies_available(books_df)

        # Assertions
        self.assertIn("copies_available", updated_df.columns, "Expected 'copies_available' column to be added.")
        self.assertEqual(updated_df.loc[0, "copies_available"], 0)
        self.assertEqual(updated_df.loc[1, "copies_available"], 5)

    # ----------------------------------------
    # Test initialize_waiting_list
    # ----------------------------------------
    def test_initialize_waiting_list(self):
        books_df = pd.DataFrame({
            "title": ["Book A", "Book B"]
        })

        # Call the function
        updated_df = initialize_waiting_list(books_df)

        # Assertions
        self.assertIn("waiting_list", updated_df.columns, "Expected 'waiting_list' column to be added.")
        self.assertEqual(updated_df["waiting_list"].tolist(), ["empty", "empty"])

    # ----------------------------------------
    # Test initialize_loaned_count
    # ----------------------------------------
    def test_initialize_loaned_count(self):
        books_df = pd.DataFrame({
            "title": ["Book A", "Book B"]
        })

        # Call the function
        updated_df = initialize_loaned_count(books_df)

        # Assertions
        self.assertIn("loaned_count", updated_df.columns, "Expected 'loaned_count' column to be added.")
        self.assertEqual(updated_df["loaned_count"].tolist(), [0, 0])

    # ----------------------------------------
    # Test initialize_users_messages
    # ----------------------------------------
    @patch("start.main.pd.DataFrame.to_csv")
    def test_initialize_users_messages(self, mock_to_csv):
        # Mock the input DataFrame
        users_df = pd.DataFrame({
            "name": ["Alice", "Bob"],
            "password": ["hashed_password_1", "hashed_password_2"]
        })

        # Call the function
        updated_df = initialize_users_messages(users_df)

        # Assertions
        self.assertIn("messages", updated_df.columns, "Expected 'messages' column to be added.")
        self.assertEqual(updated_df["messages"].tolist(), ["empty", "empty"])
        mock_to_csv.assert_called_once_with(Paths.USERS.value, index=False)

    # ----------------------------------------
    # Test get_users
    # ----------------------------------------
    @patch("start.main.pd.read_csv")
    def test_get_users(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({
            "name": ["Alice", "Bob"],
            "password": ["hashed_password_1", "hashed_password_2"]
        })

        # Call the function
        users = get_users()

        # Assertions
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].name, "Alice")
        self.assertEqual(users[1].name, "Bob")

    # ----------------------------------------
    # Test init_notification_system
    # ----------------------------------------
    @patch("start.main.get_users")
    @patch("start.main.NotificationSystem.get_instance")
    def test_init_notification_system(self, mock_get_instance, mock_get_users):
        # Mock users and notification system
        mock_user = MagicMock(name="MockUser")
        mock_get_users.return_value = [mock_user]
        mock_notification_system = MagicMock()
        mock_get_instance.return_value = mock_notification_system

        # Call the function
        init_notification_system()

        # Assertions
        mock_notification_system.add_observer.assert_called_once_with(mock_user)

    # ----------------------------------------
    # Test main
    # ----------------------------------------
    @patch("start.main.FileHandler.read_csv_files")
    @patch("start.main.FileHandler.read_users_file")
    @patch("start.main.FileHandler.create_csv")
    @patch("start.main.FileHandler.init_loaned_books")
    @patch("start.main.FileHandler.init_available_books")
    @patch("start.main.FileHandler.init_logs")
    @patch("start.main.init_notification_system")
    def test_main(self, mock_init_notification, mock_init_logs, mock_init_available, mock_init_loaned, mock_create_csv,
                  mock_read_users, mock_read_csv_files):
        # Mock dataframes
        books_df = pd.DataFrame({"title": ["Book A"], "is_loaned": ["No"], "copies": [5]})
        users_df = pd.DataFrame({"name": ["Alice"], "password": ["hashed_password"]})
        mock_read_csv_files.return_value = (books_df, None, None)
        mock_read_users.return_value = users_df

        # Call the function
        main()

        # Assertions
        mock_read_csv_files.assert_called_once()
        mock_read_users.assert_called_once()
        mock_init_notification.assert_called_once()
        mock_init_logs.assert_called_once()
        mock_init_available.assert_called_once()
        mock_init_loaned.assert_called_once()


if __name__ == "__main__":
    unittest.main()
