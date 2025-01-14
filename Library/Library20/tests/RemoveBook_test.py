from buttons.RemoveBook import remove_selected_book, remove_book_from_csvs
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd


class TestRemoveBook(unittest.TestCase):
    def setUp(self):
        """
        Set up reusable mock objects and test data for each test.
        """
        # Mock DataFrame simulating books data
        self.books_df = pd.DataFrame({
            "title": ["Book A", "Book B"],
            "copies": [2, 1],
            "copies_available": [2, 1]
        })

        # Mock Treeview and Alert Label
        self.tree = MagicMock()  # Simulated Treeview widget
        self.alert_label = MagicMock()  # Simulated Alert Label widget

    @patch("buttons.RemoveBook.utils.load_books")
    def test_remove_selected_book_no_selection(self, mock_load_books):
        """
        Test behavior when no book is selected for removal.
        """
        # Simulate no selection in Treeview
        self.tree.selection.return_value = []

        # Call the function
        remove_selected_book(self.tree, self.books_df, self.alert_label)

        # Assertions
        self.alert_label.config.assert_called_once_with(
            text="Please select a book to remove!", fg="red"
        )  # Verify the error message
        mock_load_books.assert_not_called()  # Ensure Treeview is not reloaded

    @patch("buttons.RemoveBook.remove_book_from_csvs")
    def test_remove_selected_book_logic(self, mock_remove_book):
        """
        Test successful removal of a selected book.
        """
        # Simulate the removal of "Book A" and define updated DataFrame
        updated_books_df = self.books_df[self.books_df["title"] != "Book A"]
        mock_remove_book.return_value = updated_books_df  # Simulate CSV removal logic

        # Simulate a row being selected in the Treeview
        self.tree.selection.return_value = ["item1"]
        self.tree.item.return_value = {"values": ["Book A"]}  # Selected row contains "Book A"

        # Call the function
        remove_selected_book(self.tree, self.books_df, self.alert_label)

        # Assertions
        mock_remove_book.assert_called_once_with(self.books_df, "Book A")  # Verify correct book removal
        self.alert_label.config.assert_called_once_with(
            text="'Book A' has been removed successfully!", fg="green"
        )  # Verify success message

    @patch("buttons.RemoveBook.remove_book_from_csvs")
    @patch("buttons.RemoveBook.utils.load_books")
    def test_remove_selected_book_updates_treeview(self, mock_load_books, mock_remove_book):
        """
        Test that the Treeview is reloaded after successful removal.
        """
        # Simulate the removal of "Book A"
        updated_books_df = self.books_df[self.books_df["title"] != "Book A"]
        mock_remove_book.return_value = updated_books_df

        # Simulate a row being selected in the Treeview
        self.tree.selection.return_value = ["item1"]
        self.tree.item.return_value = {"values": ["Book A"]}

        # Call the function
        remove_selected_book(self.tree, self.books_df, self.alert_label)

        # Assertions
        mock_load_books.assert_called_once_with(self.tree, updated_books_df)  # Verify Treeview reload
        self.alert_label.config.assert_called_once_with(
            text="'Book A' has been removed successfully!", fg="green"
        )  # Verify success message


if __name__ == "__main__":
    unittest.main()
