import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import tkinter as tk
from helpers.utils import utils


class TestUtils(unittest.TestCase):

    @patch("helpers.utils.tk.Tk")
    def test_load_books(self, mock_tk):
        # Mock TreeView
        tree = MagicMock()
        data = {"title": ["Book A", "Book B"], "author": ["Author A", "Author B"]}
        books_df = pd.DataFrame(data)

        # Call the function
        utils.load_books(tree, books_df)

        # Verify the TreeView is cleared and populated
        tree.get_children.assert_called_once()
        self.assertEqual(tree.insert.call_count, len(books_df))

    def test_calculate_waiting_list_size(self):
        self.assertEqual(utils.calculate_waiting_list_size("John,Jane"), 2)
        self.assertEqual(utils.calculate_waiting_list_size("empty"), 0)


    def test_get_book_with_lowest_requests_and_loans(self):
        # Mock data
        data = {"title": ["Book A", "Book B"], "requests": [5, 3]}
        popular_books_df = pd.DataFrame(data)

        # Test finding the book with the lowest requests
        result = utils.get_book_with_lowest_requests_and_loans(popular_books_df)
        self.assertEqual(result, ("Book B", 3))

        # Test with an empty DataFrame
        empty_df = pd.DataFrame(columns=["title", "requests"])
        result = utils.get_book_with_lowest_requests_and_loans(empty_df)
        self.assertIsNone(result)


    @patch("helpers.utils.FileHandler.read_popular_books_file", return_value=pd.DataFrame({"title": ["Book A"], "requests": [5]}))
    @patch("helpers.utils.utils.update_book_in_popular_books")
    def test_check_and_update_book_in_popular_books(self, mock_update_book, mock_read_file):
        # Call the function
        utils.check_and_update_book_in_popular_books("Book B", 10)

        # Assertions
        mock_update_book.assert_called_once()

    @patch("helpers.utils.NotificationSystem.get_instance")
    @patch("helpers.utils.FileHandler.read_users_file", return_value=pd.DataFrame({"name": ["User1", "User2"]}))
    def test_add_message_to_users(self, mock_read_users_file, mock_notification_system):
        # Mock notification system
        mock_instance = MagicMock()
        mock_notification_system.return_value = mock_instance

        # Call the function
        utils.add_message_to_users("Test Message")

        # Assertions
        mock_instance.notify_observers.assert_called_once_with("Test Message", mock_read_users_file.return_value)

    @patch("helpers.utils.pd.DataFrame.to_csv")  # Mock the to_csv method
    @patch("helpers.utils.utils.calculate_waiting_list_size", return_value=2)
    def test_update_book_waiting_list(self, mock_calculate, mock_to_csv):
        # Mock data
        data = {"title": ["Book A"], "waiting_list": ["empty"], "loaned_count": [1]}
        books_df = pd.DataFrame(data)
        file_path = "/fake/path.csv"

        # Call the function
        result = utils.update_book_waiting_list("Book A", "John", books_df, file_path)

        # Assertions
        self.assertTrue(result)
        self.assertEqual(books_df.at[0, "waiting_list"], "John")


if __name__ == "__main__":
    unittest.main()
