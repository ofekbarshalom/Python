import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import tkinter as tk
from helpers.utils import utils
from helpers.path import Paths


class TestUtils(unittest.TestCase):
    # ----------------------------------------
    # Test for center_window
    # ----------------------------------------
    def test_center_window(self):
        # Create a mock Tkinter window
        mock_window = MagicMock(spec=tk.Tk)

        # Define the width and height for the test
        test_width = 500
        test_height = 620

        # Mock screen dimensions
        mock_window.winfo_screenwidth.return_value = 1920
        mock_window.winfo_screenheight.return_value = 1080

        # Call the center_window function
        utils.center_window(mock_window, test_width, test_height)

        # Calculate the expected geometry
        expected_x = (1920 - test_width) // 2
        expected_y = (1080 - test_height) // 2
        expected_geometry = f"{test_width}x{test_height}+{expected_x}+{expected_y}"

        # Assert that geometry was called with the correct arguments
        mock_window.geometry.assert_called_once_with(expected_geometry)

    # ----------------------------------------
    # Test for load_books
    # ----------------------------------------
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

    # ----------------------------------------
    # Test for calculate_waiting_list_size
    # ----------------------------------------
    def test_calculate_waiting_list_size(self):
        self.assertEqual(utils.calculate_waiting_list_size("John,Jane"), 2)
        self.assertEqual(utils.calculate_waiting_list_size("empty"), 0)

    # ----------------------------------------
    # Test for update_book_waiting_list
    # ----------------------------------------
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

    # ----------------------------------------
    # Test for get_book_with_lowest_requests_and_loans
    # ----------------------------------------
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

    # ----------------------------------------
    # Test for update_book_in_popular_books
    # ----------------------------------------
    @patch("helpers.utils.pd.DataFrame.to_csv")
    def test_update_book_in_popular_books(self, mock_to_csv):
        # Initial popular_books DataFrame
        popular_books_df = pd.DataFrame({
            "title": ["Book1", "Book2"],
            "requests": [5, 3]
        })

        # test: Update an existing book with a non-zero request count
        utils.update_book_in_popular_books("Book1", popular_books_df, 10)
        self.assertEqual(popular_books_df.loc[popular_books_df["title"] == "Book1", "requests"].iloc[0], 10)
        mock_to_csv.assert_called_with(Paths.POPULAR_BOOKS.value, index=False)

    # ----------------------------------------
    # Test for check_and_update_book_in_popular_books
    # ----------------------------------------
    @patch("helpers.utils.FileHandler.read_popular_books_file", return_value=pd.DataFrame({"title": ["Book A"], "requests": [5]}))
    @patch("helpers.utils.utils.update_book_in_popular_books")
    def test_check_and_update_book_in_popular_books(self, mock_update_book, mock_read_file):
        # Call the function
        utils.check_and_update_book_in_popular_books("Book B", 10)

        # Assertions
        mock_update_book.assert_called_once()

    # ----------------------------------------
    # Test for add_message_to_users
    # ----------------------------------------
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


if __name__ == "__main__":
    unittest.main()
