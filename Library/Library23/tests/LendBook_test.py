import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from buttons.LendBook import *
from helpers.path import Paths
from tkinter import Label

class TestLendBookFunctions(unittest.TestCase):
    # ----------------------------------------
    # Test for lend_selected_book
    # ----------------------------------------
    @patch("buttons.LendBook.utils.calculate_waiting_list_size", return_value=2)
    @patch("buttons.LendBook.utils.check_and_update_book_in_popular_books")
    @patch("pandas.DataFrame.to_csv")  # Mock to avoid writing to a file
    def test_update_loaned_count_success(self, mock_to_csv, mock_check_popular_books, mock_calculate_waiting_list_size):
        # Mock DataFrame
        books_df = pd.DataFrame({
            "title": ["Book A", "Book B"],
            "loaned_count": [5, 3],
            "waiting_list": ["John,Jane", ""]
        })

        # Call the function with an existing book
        result = update_loaned_count("Book A", books_df)

        # Assertions
        self.assertTrue(result)  # Function should return True
        self.assertEqual(books_df.at[0, "loaned_count"], 6)  # Loaned count should be incremented

        # Assert DataFrame to_csv was called
        mock_to_csv.assert_called_once_with(Paths.BOOKS.value, index=False)

        # Assert waiting list size and popular books logic were checked
        mock_calculate_waiting_list_size.assert_called_once_with("John,Jane")
        mock_check_popular_books.assert_called_once_with("Book A", 8)  # 6 loaned_count + 2 requests

    # ----------------------------------------
    # Test for add_book_to_loaned_books
    # ----------------------------------------
    @patch("pandas.DataFrame.to_csv")
    def test_add_books_to_loaned_books(self, mock_to_csv):
        # Set up a mock DataFrame for loaned_books_df
        loaned_books_df = pd.DataFrame({"title": ["Existing Book"]})

        # Call the function and capture the returned DataFrame
        updated_loaned_books_df = add_book_to_loaned_books("Test Book", loaned_books_df)

        # Assert that "Test Book" is now in the updated DataFrame
        self.assertIn("Test Book", updated_loaned_books_df["title"].values)

        # Check if to_csv was called with the correct file path
        mock_to_csv.assert_called_once_with(Paths.LOANED_BOOKS.value, index=False)

        print("Test passed: Book successfully added to loaned_books_df.")

    # ----------------------------------------
    # Test for remove_book_from_available_books
    # ----------------------------------------
    @patch("pandas.DataFrame.to_csv")
    def test_remove_book_from_available_books(self, mock_to_csv):
        # Set up a mock DataFrame for available_books_df
        available_books_df = pd.DataFrame({"title": ["Book A", "Book B", "Book C"]})

        # Call the function and capture the returned DataFrame
        updated_available_books_df = remove_book_from_available_books("Book B", available_books_df)

        # Assert that "Book B" is no longer in the DataFrame
        self.assertNotIn("Book B", updated_available_books_df["title"].values)

        # Check if to_csv was called with the correct file path
        mock_to_csv.assert_called_once_with(Paths.AVAILABLE_BOOKS.value, index=False)

        print("Test passed: Book successfully removed from available_books_df.")

    # ----------------------------------------
    # Test for change_is_loaned
    # ----------------------------------------
    @patch("pandas.DataFrame.to_csv")
    def test_change_is_loaned(self, mock_to_csv):
        # Set up a mock DataFrame for books_df
        books_df = pd.DataFrame({
            "title": ["Book A", "Book B", "Book C"],
            "is_loaned": ["No", "No", "No"]
        })

        # Call the function and capture the returned DataFrame
        updated_books_df = change_is_loaned("Book B", books_df)

        # Assert that "is_loaned" for "Book B" is updated to "Yes"
        self.assertEqual(updated_books_df.loc[updated_books_df["title"] == "Book B", "is_loaned"].values[0], "Yes")

        # Check if to_csv was called with the correct file path
        mock_to_csv.assert_called_once_with(Paths.BOOKS.value, index=False)

        print("Test passed: 'is_loaned' status successfully updated to 'Yes'.")

    # ----------------------------------------
    # Test for decrement_copies_available_in_available_books
    # ----------------------------------------
    @patch("pandas.DataFrame.to_csv")
    def test_decrement_copies_available_in_available_books(self, mock_to_csv):
        # Set up a mock DataFrame for available_books_df
        available_books_df = pd.DataFrame({
            "title": ["Book A", "Book B", "Book C"],
            "copies_available": [5, 3, 2]
        })

        # Call the function to decrement copies for "Book B"
        decrement_copies_available_in_available_books("Book B", available_books_df, 3)

        # Assert that "copies_available" for "Book B" is decremented by 1
        self.assertEqual(available_books_df.loc[available_books_df["title"] == "Book B", "copies_available"].values[0], 2)

        # Check if to_csv was called with the correct file path
        mock_to_csv.assert_called_once_with(Paths.AVAILABLE_BOOKS.value, index=False)

        print("Test passed: Copies successfully decremented in available_books_df.")

    # ----------------------------------------
    # Test for check_book_request
    # ----------------------------------------
    @staticmethod
    def create_mock_books_df():
        return pd.DataFrame({
            "title": ["Book A", "Book B", "Book C"],
            "waiting_list": ["ofek,roy,naama", "empty", "sigal,dror"]
        })

    def test_check_book_request_found(self):
        # Get mock DataFrame
        books_df = self.create_mock_books_df()

        # Test case where the book exists and has a waiting list
        first_request = check_book_request("Book A", books_df)
        self.assertEqual(first_request, "ofek")
        print("Test passed: Correct first name returned for book with waiting list.")

    def test_check_book_request_empty_list(self):
        # Get mock DataFrame
        books_df = self.create_mock_books_df()

        # Test case where the book exists but has an empty waiting list
        first_request = check_book_request("Book B", books_df)
        self.assertIsNone(first_request)
        print("Test passed: None returned for book with empty waiting list.")

    # ----------------------------------------
    # Test for remove_first_request
    # ----------------------------------------
    @patch("pandas.DataFrame.to_csv")
    def test_remove_first_request_success(self, mock_to_csv):
        books_df = self.create_mock_books_df()

        # Call the function to remove the first request for "Book A"
        result = remove_first_request("Book A", books_df)

        # Check the result is True
        self.assertTrue(result)

        # Verify that the waiting list is updated correctly
        updated_waiting_list = books_df.loc[books_df["title"] == "Book A", "waiting_list"].values[0]
        self.assertEqual(updated_waiting_list, "roy,naama")

        # Verify that to_csv was called once with the correct file path
        mock_to_csv.assert_called_once_with(Paths.BOOKS.value, index=False)

        print("Test passed: Successfully removed the first request from the waiting list.")


    @patch("pandas.DataFrame.to_csv")
    def test_remove_first_request_book_not_found(self, mock_to_csv):
        books_df = self.create_mock_books_df()

        # Call the function to remove the first request for a non-existent book
        result = remove_first_request("Nonexistent Book", books_df)

        # Check the result is False
        self.assertFalse(result)

        # Verify that to_csv was not called
        mock_to_csv.assert_not_called()

        print("Test passed: Correctly handled a non-existent book.")

    # ----------------------------------------
    # Test for check_waiting_list_name
    # ----------------------------------------
    @patch("buttons.LendBook.utils.get_name_popup")
    @patch("buttons.LendBook.remove_first_request")
    def test_check_waiting_list_name_success(self, mock_remove_first_request, mock_get_name_popup):
        books_df = self.create_mock_books_df()
        mock_get_name_popup.return_value = "ofek"  # Simulate user input matching the first in the queue
        mock_remove_first_request.return_value = True

        # Mock the alert_label
        alert_label = MagicMock()

        # Call the function and check the result
        result = check_waiting_list_name("Book A", alert_label, books_df)
        self.assertTrue(result)

        # Verify that the popup was displayed with the correct text
        mock_get_name_popup.assert_called_once_with(
            "'Book A' has a waiting list.\nIf you're first, the book will be loaned to you.")

        # Verify that remove_first_request was called for the correct book
        mock_remove_first_request.assert_called_once_with("Book A", books_df)

        # Ensure alert_label was not used (no errors expected)
        alert_label.config.assert_not_called()

        print("Test passed: Successfully loaned book to the first in the waiting list.")

    @patch("buttons.LendBook.utils.get_name_popup")
    def test_check_waiting_list_name_not_first_in_queue(self, mock_get_name_popup):
        books_df = self.create_mock_books_df()
        mock_get_name_popup.return_value = "roy"  # Simulate user input not matching the first in the queue

        # Mock the alert_label
        alert_label = MagicMock()

        # Call the function and check the result
        result = check_waiting_list_name("Book A", alert_label, books_df)
        self.assertFalse(result)

        # Verify that the popup was displayed with the correct text
        mock_get_name_popup.assert_called_once_with(
            "'Book A' has a waiting list.\nIf you're first, the book will be loaned to you.")

        # Ensure alert_label was updated with an error message
        alert_label.config.assert_called_once_with(text="'roy' not the first at the waiting list", fg="red")

        print("Test passed: Correctly handled user not being first in the waiting list.")

    # ----------------------------------------
    # Test for update_files
    # ----------------------------------------
    @staticmethod
    def create_mock_dataframes():
        return {
            "books_df": pd.DataFrame({
                "title": ["Book A", "Book B", "Book C"],
                "copies_available": [1, 2, 3],
                "loaned_count": [5, 2, 1],
                "waiting_list": ["John,Doe", "empty", "Alice,Bob"],
                "is_loaned": ["No", "No", "No"]
            }),
            "available_books_df": pd.DataFrame({
                "title": ["Book A", "Book B", "Book C"],
                "copies_available": [1, 2, 3]
            }),
            "loaned_books_df": pd.DataFrame({
                "title": []
            })
        }

    @patch("buttons.LendBook.FileHandler.read_csv_files")
    @patch("buttons.LendBook.add_book_to_loaned_books")
    @patch("buttons.LendBook.remove_book_from_available_books")
    @patch("buttons.LendBook.change_is_loaned")
    @patch("buttons.LendBook.decrement_copies_available_in_available_books")
    @patch("buttons.LendBook.decrement_copies_available_in_books")
    @patch("buttons.LendBook.utils.calculate_waiting_list_size")
    @patch("buttons.LendBook.utils.check_and_update_book_in_popular_books")
    @patch("buttons.LendBook.update_loaned_count")
    def test_update_files_copies_available_one(
            self,
            mock_update_loaned_count,
            mock_check_and_update_popular_books,
            mock_calculate_waiting_list_size,
            mock_decrement_copies_available_in_books,
            mock_decrement_copies_available_in_available_books,
            mock_change_is_loaned,
            mock_remove_book_from_available_books,
            mock_add_book_to_loaned_books,
            mock_read_csv_files
    ):
        # Arrange
        mock_data = self.create_mock_dataframes()
        mock_read_csv_files.return_value = (
            mock_data["books_df"],
            mock_data["available_books_df"],
            mock_data["loaned_books_df"]
        )
        mock_calculate_waiting_list_size.return_value = 2

        # Act
        update_files("Book A")

        # Assert
        mock_add_book_to_loaned_books.assert_called_once_with("Book A", mock_data["loaned_books_df"])
        mock_remove_book_from_available_books.assert_called_once_with("Book A", mock_data["available_books_df"])
        mock_change_is_loaned.assert_called_once_with("Book A", mock_data["books_df"])

        # Fix: Assert call arguments separately to avoid direct DataFrame comparison
        self.assertTrue(mock_update_loaned_count.called)
        called_args = mock_update_loaned_count.call_args[0]
        self.assertEqual(called_args[0], "Book A")  # Verify book title
        self.assertTrue(called_args[1].equals(mock_data["books_df"]))  # Verify DataFrame equality

        print("Test passed: Files updated correctly when copies_available is 1.")

    # ----------------------------------------
    # Test for alert_loaned_books
    # ----------------------------------------
    @patch("buttons.LendBook.utils.get_name_popup", return_value="Ofek")
    @patch("buttons.LendBook.utils.update_book_waiting_list", return_value=True)
    @patch("buttons.LendBook.utils.load_books")
    def test_alert_loaned_books(self, mock_load_books, mock_update_book_waiting_list, mock_get_name_popup):
        # Mock data
        loaned_books_df = pd.DataFrame({"title": ["Book A", "Book B"]})
        books_df = pd.DataFrame({"title": ["Book A", "Book B"], "waiting_list": ["empty", ""]})
        alert_label = Label()
        tree = MagicMock()

        # Test when the book is already loaned
        result = alert_loaned_books("Book A", loaned_books_df, books_df, alert_label, tree)
        self.assertTrue(result)
        mock_get_name_popup.assert_called_once_with("'Book A' is currently loaned out.")
        mock_update_book_waiting_list.assert_called_once_with(
            "Book A", "Ofek", books_df, Paths.BOOKS.value
        )
        mock_load_books.assert_called_once_with(tree, books_df)
        self.assertEqual(alert_label.cget("text"), "Client 'Ofek' added to the waiting list of book 'Book A'.")

    # ----------------------------------------
    # Test for lend_selected_book
    # ----------------------------------------
    @patch("buttons.LendBook.Logger.get_logger")
    @patch("buttons.LendBook.alert_loaned_books")
    @patch("buttons.LendBook.check_waiting_list_name")
    @patch("buttons.LendBook.update_files")
    @patch("buttons.LendBook.utils.load_books")
    @patch("buttons.LendBook.FileHandler.read_csv_files")
    def test_lend_selected_book(self, mock_read_csv_files, mock_load_books, mock_update_files,
                                mock_check_waiting_list_name, mock_alert_loaned_books, mock_get_logger):
        # Mock the logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Mock return values for dependencies
        mock_read_csv_files.return_value = (
            [{"title": "Book A"}],  # books_df
            [],  # available_books_df
            []   # loaned_books_df
        )
        mock_alert_loaned_books.return_value = False
        mock_check_waiting_list_name.return_value = True

        # Mock objects for tree and alert_label
        tree = MagicMock()
        alert_label = Label()

        # Simulate tree selection and item structure
        tree.selection.return_value = ["item1"]  # Simulate a valid selection
        tree.item.return_value = ["Book A"]  # Simulate a valid list structure for "values"

        # Call the function
        lend_selected_book(tree, alert_label)

        # Assert function behavior
        mock_alert_loaned_books.assert_called_once_with("Book A", [], [{"title": "Book A"}], alert_label, tree)
        mock_check_waiting_list_name.assert_called_once_with("Book A", alert_label, [{"title": "Book A"}])
        mock_update_files.assert_called_once_with("Book A")
        mock_load_books.assert_called_once()

        # Assert logger was called correctly
        mock_logger.info.assert_called_with("book borrowed successfully")


if __name__ == "__main__":
    unittest.main()
