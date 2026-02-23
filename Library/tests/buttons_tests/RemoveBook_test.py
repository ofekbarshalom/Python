import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from buttons.RemoveBook import *
from helpers.path import Paths


class TestRemoveBook(unittest.TestCase):
    # ----------------------------------------
    # Test for update_loaned_and_available_books
    # ----------------------------------------
    @patch("buttons.RemoveBook.pd.read_csv", side_effect=FileNotFoundError)  # Simulate missing files
    @patch("buttons.RemoveBook.pd.DataFrame.to_csv")  # Mock pandas to_csv
    def test_update_loaned_and_available_books_file_not_found(self, mock_to_csv, mock_read_csv):
        # Call the function with a book to remove
        update_loaned_book_and_available_books("Nonexistent Book")

        # Assert that read_csv was called for both files
        mock_read_csv.assert_any_call(Paths.LOANED_BOOKS.value)
        mock_read_csv.assert_any_call(Paths.AVAILABLE_BOOKS.value)

        # Assert that to_csv was never called because files were not found
        mock_to_csv.assert_not_called()

    # ----------------------------------------
    # Test for remove_book_from_csvs
    # ----------------------------------------
    @patch("buttons.RemoveBook.pd.DataFrame.to_csv")  # Mock pandas to_csv
    @patch("buttons.RemoveBook.update_loaned_book_and_available_books")  # Mock the update function
    @patch("buttons.RemoveBook.Paths")  # Mock the Paths Enum
    def test_remove_book_from_csvs(self, mock_paths, mock_update_loaned_books, mock_to_csv):
        # Mock Paths.BOOKS.value
        mock_paths.BOOKS.value = "/fake/path/books.csv"

        # Sample input DataFrame
        data = {
            "title": ["Book A", "Book B", "Book C"],
            "author": ["Author A", "Author B", "Author C"],
            "copies": [3, 2, 4],
        }
        books_df = pd.DataFrame(data)

        # Call the function
        updated_books_df = remove_book_from_csvs(books_df, "Book B")

        # Verify that the book was removed from the DataFrame
        self.assertEqual(len(updated_books_df), 2)
        self.assertNotIn("Book B", updated_books_df["title"].values)

        # Ensure the update function was called
        mock_update_loaned_books.assert_called_once_with("Book B")

        # Ensure the DataFrame was written back to CSV
        mock_to_csv.assert_called_once_with("/fake/path/books.csv", index=False)

    @patch("buttons.SearchBook.Logger.get_logger")  # Mock the logger
    @patch("buttons.RemoveBook.remove_book_from_csvs")  # Mock remove_book_from_csvs
    @patch("buttons.RemoveBook.utils")  # Mock the utils module
    def test_remove_selected_book_success(self, mock_utils, mock_remove_book_from_csvs, mock_get_logger):
        # Mock the logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Input DataFrame setup
        data = {
            "title": ["Book A", "Book B", "Book C"],
            "copies": [2, 3, 1],
            "copies_available": [2, 3, 1],
        }
        books_df = pd.DataFrame(data)

        # Treeview mock setup
        tree = MagicMock()
        tree.selection.return_value = "selected_item"  # Simulate a selected item
        tree.item.return_value = ["Book A", "Author A", 2]  # Return a list directly as expected by the method

        # Alert label mock setup
        alert_label = MagicMock()

        # Expected DataFrame after removing "Book A"
        expected_books_df = books_df[books_df["title"] != "Book A"]

        # Mock `remove_book_from_csvs` to return the updated DataFrame
        mock_remove_book_from_csvs.return_value = expected_books_df

        # Call the function
        remove_selected_book(tree, books_df, alert_label)

        # Assert `remove_book_from_csvs` was called correctly
        mock_remove_book_from_csvs.assert_called_once()
        called_books_df, called_book_title = mock_remove_book_from_csvs.call_args[0]

        # Verify the correct book title was passed
        self.assertEqual(called_book_title, "Book A")

        # Verify the correct `books_df` was passed to `remove_book_from_csvs`
        pd.testing.assert_frame_equal(called_books_df, books_df)

        # Assert `utils.add_message_to_users` was called with the correct message
        mock_utils.add_message_to_users.assert_called_once_with("The book Book A as been removed from the library")

        # Assert alert label was updated correctly
        alert_label.config.assert_called_once_with(text="'Book A' has been removed successfully!", fg="green")

        # Assert logger calls
        mock_logger.info.assert_any_call("book removed successfully")


if __name__ == "__main__":
    unittest.main()
