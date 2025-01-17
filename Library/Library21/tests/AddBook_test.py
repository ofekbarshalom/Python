import unittest
from unittest.mock import patch, MagicMock
from helpers.FileHandler import FileHandler
from buttons.AddBook import *


class TestAddBookFunctions(unittest.TestCase):
    def test_check_copies_and_year(self):
        alert_label = MagicMock()

        # Test valid inputs
        check_copies_and_year("5", "2020", alert_label)
        alert_label.config.assert_not_called()

        # Test invalid copies (negative value)
        with self.assertRaises(ValueError) as context:
            check_copies_and_year("-1", "2020", alert_label)
        alert_label.config.assert_called_with(text="Copies must be a positive integer.", fg="red")
        self.assertEqual(str(context.exception), "Copies must be a positive integer.")
        alert_label.reset_mock()

        # Test non-integer copies
        with self.assertRaises(ValueError) as context:
            check_copies_and_year("abc", "xyz", alert_label)
        alert_label.config.assert_called_with(text="Copies and year must be numbers.", fg="red")
        self.assertEqual(str(context.exception), "Copies and year must be numbers.")
        alert_label.reset_mock()

    @patch('buttons.AddBook.FileHandler.read_csv_files')
    def test_check_book_title(self, mock_read_csv_files):
        # Mock books data
        mock_books_df = MagicMock()
        mock_books_df['title'].str.lower().eq.return_value.any.return_value = True
        mock_read_csv_files.return_value = (mock_books_df, None, None)

        # Test case: Book exists
        book_title = "Existing Book"
        result = check_book_title(book_title)
        self.assertTrue(result)

        # Test case: Book does not exist
        mock_books_df['title'].str.lower().eq.return_value.any.return_value = False
        result = check_book_title("Nonexistent Book")
        self.assertFalse(result)

    def setUp(self):
        # Common setup for all fields except title
        self.entries = {
            "title": MagicMock(get=MagicMock()),  # Will be overridden in individual tests
            "author": MagicMock(get=MagicMock(return_value="Test Author")),
            "copies": MagicMock(get=MagicMock(return_value="5")),
            "genre": MagicMock(get=MagicMock(return_value="Fiction")),
            "year": MagicMock(get=MagicMock(return_value="2023")),
        }
        self.alert_label = MagicMock()
        self.dropdown_var = MagicMock(get=MagicMock(return_value="No"))
        self.current_window = MagicMock()

    def test_validate_required_fields_success(self):
        # Set title field for this test
        self.entries["title"].get.return_value = "Test Title"

        # Call the function and assert the return values
        result = validate_required_fields(self.entries, self.alert_label)
        self.assertEqual(result, ("Test Title", "Test Author", "5", "Fiction", "2023"))
        self.alert_label.config.assert_not_called()

    def test_validate_required_fields_missing_title(self):
        # Set title field to empty
        self.entries["title"].get.return_value = ""

        # Call the function and assert it raises a ValueError
        with self.assertRaises(ValueError) as context:
            validate_required_fields(self.entries, self.alert_label)
        self.assertEqual(str(context.exception), "Missing required fields.")
        self.alert_label.config.assert_called_with(text="All fields must be filled out!", fg="red")


    @patch('buttons.AddBook.check_book_title')
    @patch('buttons.AddBook.check_copies_and_year')
    @patch('buttons.AddBook.BookFactory.create_book')
    @patch('buttons.AddBook.User.add_book_to_library')
    @patch('buttons.AddBook.utils.add_message_to_users')
    def test_submit_new_book_success(self, mock_add_message_to_users, mock_add_book_to_library, mock_create_book, mock_check_copies_and_year, mock_check_book_title):
        # Mock return values
        mock_check_book_title.return_value = False
        self.entries["title"].get.return_value = "Test Title"

        # Call the function
        submit_new_book(self.entries, self.dropdown_var, self.current_window, self.alert_label)

        # Assert validations and actions
        mock_check_copies_and_year.assert_called_with("5", "2023", self.alert_label)
        mock_check_book_title.assert_called_with("Test Title")
        mock_create_book.assert_called_with("Test Title", "Test Author", "No", "5", "Fiction", "2023")
        mock_add_book_to_library.assert_called_once()
        mock_add_message_to_users.assert_called_with("The book Test Title added to the library")
        self.alert_label.config.assert_called_with(text="The book Test Title added to the library", fg="green")
        self.current_window.after.assert_called_with(1000, self.current_window.destroy)


if __name__ == "__main__":
    unittest.main()
