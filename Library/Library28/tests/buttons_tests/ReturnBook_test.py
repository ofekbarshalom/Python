import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
from tkinter import Label
from buttons.ReturnBook import *

class TestReturnBook(unittest.TestCase):
    # ----------------------------------------
    # Test for load_books
    # ----------------------------------------
    def test_load_books(self):
        tree = MagicMock()
        tree.get_children.return_value = ["child1", "child2"]  # Mock existing children
        books_df = pd.DataFrame({
            "title": ["Book A", "Book B"],
            "author": ["Author A", "Author B"],
            "copies": [5, 2]
        })

        load_books(tree, books_df)

        # Assert Treeview is cleared and populated
        tree.delete.assert_has_calls([call("child1"), call("child2")])  # Ensure children are cleared
        tree.insert.assert_any_call("", "end", values=["Book A", "Author A", 5])
        tree.insert.assert_any_call("", "end", values=["Book B", "Author B", 2])

    # ----------------------------------------
    # Test for add_book_to_available_books
    # ----------------------------------------
    @patch("pandas.DataFrame.to_csv")
    def test_add_book_to_available_books(self, mock_to_csv):
        # Mock input data
        available_books_df = pd.DataFrame({
            "title": ["Book A"],
            "copies_available": [2]
        })
        book_title = "Book B"
        copies_available = 3

        # Call the function
        updated_df = add_book_to_available_books(book_title, available_books_df, copies_available)

        # Verify the new book was added
        self.assertEqual(len(updated_df), 2)  # Ensure a new row is added
        self.assertTrue((updated_df["title"] == "Book B").any())  # Ensure the new book is in the DataFrame
        self.assertEqual(updated_df[updated_df["title"] == "Book B"]["copies_available"].iloc[0], 3)

        # Verify the file was saved (path is not mocked directly)
        mock_to_csv.assert_called_once()

    # ----------------------------------------
    # Test for alert_returned_books
    # ----------------------------------------
    def test_alert_returned_books(self):
        books_df = pd.DataFrame({
            "title": ["Book A", "Book B"],
            "copies": [2, 3],
            "copies_available": [2, 2]
        })
        alert_label = MagicMock()

        # Test when all copies are returned
        result = alert_returned_books("Book A", books_df, alert_label)
        self.assertTrue(result)
        alert_label.config.assert_called_once_with(
            text="All copies of 'Book A' are already returned", fg="red"
        )

        # Test when copies are not fully returned
        alert_label.reset_mock()
        result = alert_returned_books("Book B", books_df, alert_label)
        self.assertFalse(result)
        alert_label.config.assert_not_called()

    # ----------------------------------------
    # Test for return_selected_book
    # ----------------------------------------
    @patch("buttons.ReturnBook.Logger.get_logger")
    @patch("buttons.ReturnBook.alert_returned_books")
    @patch("buttons.ReturnBook.update_files")
    @patch("buttons.ReturnBook.load_books")
    @patch("buttons.ReturnBook.FileHandler.read_csv_files")
    def test_return_selected_book(self, mock_read_csv_files, mock_load_books, mock_update_files,
                                  mock_alert_returned_books, mock_get_logger):
        # Mock the logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Mock return values for dependencies
        mock_read_csv_files.return_value = (
            [{"title": "Book A"}],  # books_df
            [],  # available_books_df
            []   # loaned_books_df
        )
        mock_alert_returned_books.return_value = False

        # Mock objects for tree and alert_label
        tree = MagicMock()
        alert_label = Label()

        # Simulate tree selection and item structure
        tree.selection.return_value = ["item1"]  # Simulate a valid selection
        tree.item.return_value = ["Book A"]  # Simulate a valid list structure for "values"

        # Call the function
        return_selected_book(tree, alert_label)

        # Assert function behavior
        mock_alert_returned_books.assert_called_once_with("Book A", [{"title": "Book A"}], alert_label)
        mock_update_files.assert_called_once_with("Book A")
        mock_load_books.assert_called_once_with(tree, [{"title": "Book A"}])

        # Assert logger was called correctly
        mock_logger.info.assert_called_with("book returned successfully")

    # ----------------------------------------
    # Test for update_files
    # ----------------------------------------
    @patch("buttons.ReturnBook.FileHandler.read_csv_files")
    @patch("buttons.ReturnBook.add_book_to_available_books")
    @patch("buttons.ReturnBook.remove_book_from_loaned_books")
    @patch("buttons.ReturnBook.change_is_loaned")
    @patch("buttons.ReturnBook.increment_copies_available_in_books")
    @patch("buttons.ReturnBook.increment_copies_available_in_available_books")
    @patch("buttons.ReturnBook.check_book_request")
    @patch("buttons.ReturnBook.utils.add_message_to_users")
    def test_update_files(self, mock_add_message_to_users, mock_check_book_request,
                          mock_increment_available_books, mock_increment_books,
                          mock_change_is_loaned, mock_remove_book, mock_add_book, mock_read_csv):
        # Mock file handler return values
        books_df = pd.DataFrame({
            "title": ["Book A"],
            "copies_available": [0],
            "is_loaned": ["No"]
        })
        available_books_df = pd.DataFrame({
            "title": [],
            "copies_available": []
        })
        loaned_books_df = pd.DataFrame({
            "title": ["Book A"]
        })
        mock_read_csv.return_value = (books_df, available_books_df, loaned_books_df)

        # Mock behavior for dependencies
        modified_available_books_df = pd.DataFrame({
            "title": ["Book A"],
            "copies_available": [1]
        })
        mock_add_book.return_value = modified_available_books_df
        mock_check_book_request.return_value = "John"

        # Call the function
        update_files("Book A")

        # Assertions
        mock_add_book.assert_called_once_with("Book A", available_books_df, 0)
        mock_remove_book.assert_called_once_with("Book A", loaned_books_df)
        mock_change_is_loaned.assert_called_once_with("Book A", books_df)
        mock_increment_books.assert_called_once()  # Ensure the function was called

        # Use the modified DataFrame for assertion
        mock_increment_available_books.assert_called_once_with("Book A", modified_available_books_df, 0)
        mock_add_message_to_users.assert_called_once_with("John can lend the book Book A now")


if __name__ == "__main__":
    unittest.main()
