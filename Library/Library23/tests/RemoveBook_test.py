import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from buttons.RemoveBook import *
from helpers.path import Paths


class TestRemoveBookFunctions(unittest.TestCase):
    # ----------------------------------------
    # Test for update_loaned_and_available_books
    # ----------------------------------------
    @patch("buttons.RemoveBook.pd.read_csv")  # Mock pandas read_csv
    @patch("buttons.RemoveBook.pd.DataFrame.to_csv")  # Mock pandas to_csv
    def test_update_loaned_and_available_books_success(self, mock_to_csv, mock_read_csv):
        # Mock DataFrames for loaned_books and available_books
        loaned_books_df = pd.DataFrame({"title": ["Book A", "Book B"]})
        available_books_df = pd.DataFrame({"title": ["Book A", "Book C"]})

        # Mock read_csv to return the mock DataFrames
        mock_read_csv.side_effect = [loaned_books_df, available_books_df]

        # List to store captured DataFrames
        captured_dataframes = []

        # Capture the DataFrame passed to `to_csv`
        def capture_dataframe(df, *args, **kwargs):
            captured_dataframes.append(df)

        # Assign the `side_effect` to capture DataFrames
        mock_to_csv.side_effect = capture_dataframe

        # Call the function with a book to remove
        update_loaned_book_and_available_books("Book A")

        # Assertions for loaned_books.csv
        expected_loaned_books_df = pd.DataFrame({"title": ["Book B"]})
        pd.testing.assert_frame_equal(captured_dataframes[0], expected_loaned_books_df)

        # Assertions for available_books.csv
        expected_available_books_df = pd.DataFrame({"title": ["Book C"]})
        pd.testing.assert_frame_equal(captured_dataframes[1], expected_available_books_df)

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


if __name__ == "__main__":
    unittest.main()
