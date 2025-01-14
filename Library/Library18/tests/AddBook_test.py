import unittest
from unittest.mock import MagicMock, patch
from AddBook import check_copies_and_year, submit_new_book


class AddBookLogicTest(unittest.TestCase):
    def test_check_copies_and_year_invalid(self):
        """
        Test invalid copies and year input raises an error.
        """
        # Mock the alert_label to avoid GUI dependency
        mock_label = MagicMock()

        # This should raise a ValueError for invalid copies
        with self.assertRaises(ValueError):
            check_copies_and_year("-1", "2023", mock_label)

        # This should raise a ValueError for non-numeric input
        with self.assertRaises(ValueError):
            check_copies_and_year("abc", "xyz", mock_label)

        # Ensure the mock_label config method is called
        mock_label.config.assert_called()

    def test_check_copies_and_year_valid(self):
        """
        Test valid copies and year input does not raise an error.
        """
        # Mock the alert_label to avoid GUI dependency
        mock_label = MagicMock()

        # Test valid inputs that should not raise an exception
        try:
            check_copies_and_year("10", "2023", mock_label)  # Valid copies and year
        except Exception as e:
            self.fail(f"check_copies_and_year raised an exception unexpectedly: {e}")

######################################################################################################
######################################################################################################

    @patch("AddBook.BookFactory.create_book")
    @patch("AddBook.User.add_book_to_library")
    @patch("AddBook.NotificationSystem.get_instance")
    def test_submit_new_book_valid(self, mock_notification_system, mock_add_book, mock_create_book):
        """
        Test valid inputs for submit_new_book.
        """
        # Mock dependencies
        mock_alert_label = MagicMock()
        mock_current_window = MagicMock()
        mock_entries = {
            "title": MagicMock(get=MagicMock(return_value="Valid Title")),
            "author": MagicMock(get=MagicMock(return_value="Valid Author")),
            "copies": MagicMock(get=MagicMock(return_value="5")),
            "genre": MagicMock(get=MagicMock(return_value="Fiction")),
            "year": MagicMock(get=MagicMock(return_value="2023")),
        }
        mock_dropdown_var = MagicMock(get=MagicMock(return_value="No"))

        mock_notification_instance = MagicMock()
        mock_notification_system.return_value = mock_notification_instance

        # Call the method
        try:
            submit_new_book(mock_entries, mock_dropdown_var, mock_current_window, mock_alert_label)
        except Exception as e:
            self.fail(f"submit_new_book raised an exception unexpectedly: {e}")

        # Assertions
        mock_create_book.assert_called_once_with(
            title="Valid Title",
            author="Valid Author",
            is_loaned="No",
            copies="5",
            genre="Fiction",
            year="2023",
        )
        mock_add_book.assert_called_once()
        mock_alert_label.config.assert_called_with(
            text="The book Valid Title added to the library", fg="green"
        )
        mock_current_window.after.assert_called_once_with(1000, mock_current_window.destroy)
        mock_notification_instance.notify_observers.assert_called_once()

    @patch("AddBook.Logger.log_decorator", lambda x, y: lambda func: func)
    @patch("AddBook.BookFactory.create_book")
    @patch("AddBook.User.add_book_to_library")
    def test_submit_new_book_invalid(self, mock_add_book, mock_create_book):
        """
        Test invalid inputs (missing fields) for submit_new_book.
        """
        # Mock dependencies
        mock_alert_label = MagicMock()
        mock_current_window = MagicMock()
        mock_entries = {
            "title": MagicMock(get=MagicMock(return_value="Valid Title")),
            "author": MagicMock(get=MagicMock(return_value="Valid Author")),
            "copies": MagicMock(get=MagicMock(return_value="5")),
            "genre": MagicMock(get=MagicMock(return_value="")),  # Empty genre
            "year": MagicMock(get=MagicMock(return_value="")),  # Empty year
        }
        mock_dropdown_var = MagicMock(get=MagicMock(return_value="No"))

        # Call the method
        submit_new_book(mock_entries, mock_dropdown_var, mock_current_window, mock_alert_label)

        # Assert the decorator handled the exception (via log or behavior)
        mock_alert_label.config.assert_called_with(
            text="All fields must be filled out!", fg="red"
        )
        mock_alert_label.after.assert_called_once()
        mock_create_book.assert_not_called()
        mock_add_book.assert_not_called()

#####################################################################################################
#####################################################################################################


if __name__ == "__main__":
    unittest.main()
