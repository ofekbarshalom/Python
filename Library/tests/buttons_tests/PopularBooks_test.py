import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from buttons.PopularBooks import create_table


class TestPopularBooks(unittest.TestCase):
    @patch("buttons.PopularBooks.utils.load_books")  # Mock the load_books function
    @patch("buttons.PopularBooks.ttk.Treeview")  # Mock the Treeview widget
    @patch("buttons.PopularBooks.Logger.get_logger")  # Mock the logger
    def test_create_table(self, mock_get_logger, mock_treeview, mock_load_books):
        # Mock the logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Create a mock parent window and sample data
        parent = MagicMock()
        data = MagicMock()
        data.columns = ["Column1", "Column2", "Column3"]

        # Call the function
        create_table(parent, data)

        # Assertions
        # Verify Treeview was created with the correct parameters
        mock_treeview.assert_called_once_with(parent, columns=["Column1", "Column2", "Column3"], show="headings", height=15)
        tree_instance = mock_treeview.return_value
        tree_instance.pack.assert_called_once_with(pady=10, fill=tk.BOTH, expand=True)

        # Verify load_books was called with the Treeview and data
        mock_load_books.assert_called_once_with(tree_instance, data)

        # Verify logger recorded a success message
        mock_logger.info.assert_called_with("displayed successfully")

    @patch("buttons.PopularBooks.utils.load_books")  # Mock the load_books function
    @patch("buttons.PopularBooks.ttk.Treeview")  # Mock the Treeview widget
    @patch("buttons.PopularBooks.Logger.get_logger")  # Mock the logger
    def test_create_table_fail(self, mock_get_logger, mock_treeview, mock_load_books):
        # Mock the logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Create a mock parent window
        parent = MagicMock()

        # Pass invalid data to simulate failure
        invalid_data = None

        # Call the function (no exception expected)
        create_table(parent, invalid_data)

        # Verify that the failure was logged
        mock_logger.error.assert_called_with("displayed fail")

        # Ensure Treeview and load_books were not called
        mock_treeview.assert_not_called()
        mock_load_books.assert_not_called()


if __name__ == "__main__":
    unittest.main()
