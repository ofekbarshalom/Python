import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from pandas.testing import assert_frame_equal
from buttons.SearchBook import *


class TestSearchBook(unittest.TestCase):
    # ----------------------------------------
    # Test for perform_search
    # ----------------------------------------
    @patch("buttons.SearchBook.Logger.get_logger")  # Mock the logger
    @patch("buttons.SearchBook.FileHandler.read_csv_files")
    @patch("buttons.SearchBook.refresh_table")
    @patch("buttons.SearchBook.SearchByTitle")
    @patch("buttons.SearchBook.SearchByAuthor")
    @patch("buttons.SearchBook.SearchByGenre")
    def test_perform_search_by_title(self, mock_search_by_genre, mock_search_by_author, mock_search_by_title,
                                     mock_refresh_table, mock_read_csv, mock_get_logger):
        # Mock the logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Mock input data
        books_df = pd.DataFrame({
            "title": ["Book A", "Book B"],
            "author": ["Author A", "Author B"],
            "genre": ["Genre A", "Genre B"]
        })
        mock_read_csv.return_value = (books_df, None, None)

        # Mock strategy behavior
        mock_title_strategy = MagicMock()
        filtered_df = books_df.loc[books_df["title"] == "Book A"]
        mock_title_strategy.search.return_value = filtered_df
        mock_search_by_title.return_value = mock_title_strategy

        # Mock GUI elements
        search_entry = MagicMock()
        search_entry.get.return_value = "Book A"
        search_type_combobox = MagicMock()
        search_type_combobox.get.return_value = "Title"
        table = MagicMock()

        # Call the function
        perform_search(search_entry, search_type_combobox, table)

        # Assertions
        mock_search_by_title.assert_called_once()  # Ensure Title strategy is used
        mock_title_strategy.search.assert_called_once_with("Book A", books_df)

        # Assert logger calls
        mock_logger.info.assert_any_call("Search book 'Book A' by Title completed successfully")

    # ----------------------------------------
    # Test for refresh_table
    # ----------------------------------------
    def test_refresh_table(self):
        # Mock the table
        table = MagicMock()

        # Mock the books DataFrame
        books_df = pd.DataFrame({
            "title": ["Book A", "Book B"],
            "author": ["Author A", "Author B"],
            "is_loaned": ["Yes", "No"],
            "copies": [2, 5],
            "genre": ["Fiction", "Science"],
            "year": [2020, 2018]
        })

        # Call the function
        refresh_table(table, books_df)

        # Assert that table rows were cleared
        table.delete.assert_called_once_with(*table.get_children())


if __name__ == "__main__":
    unittest.main()
