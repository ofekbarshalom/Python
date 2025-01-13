import unittest
from unittest.mock import patch, MagicMock
from AddBook import check_copies_and_year, submit_new_book


class AddBookLogicTest(unittest.TestCase):
    def test_check_copies_and_year_valid(self):
        """
        Test valid copies and year input.
        """
        try:
            check_copies_and_year("10", "2023", None)  # No label needed
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_check_copies_and_year_invalid_copies(self):
        """
        Test invalid copies input (negative number).
        """
        with self.assertRaises(ValueError):
            check_copies_and_year("-1", "2023", None)

    def test_check_copies_and_year_invalid_format(self):
        """
        Test non-numeric input for copies and year.
        """
        with self.assertRaises(ValueError):
            check_copies_and_year("abc", "xyz", None)

    @patch("AddBook.BookFactory.create_book")
    @patch("AddBook.User.add_book_to_library")
    def test_submit_new_book_valid(self, mock_add_book, mock_create_book):
        """
        Test submitting a valid new book.
        """
        entries = {
            "title": MagicMock(get=MagicMock(return_value="Valid Title")),
            "author": MagicMock(get=MagicMock(return_value="Valid Author")),
            "copies": MagicMock(get=MagicMock(return_value="5")),
            "genre": MagicMock(get=MagicMock(return_value="Fiction")),
            "year": MagicMock(get=MagicMock(return_value="2023")),
        }
        dropdown_var = MagicMock(get=MagicMock(return_value="No"))
        current_window = MagicMock()

        try:
            submit_new_book(entries, dropdown_var, current_window, None)  # No label needed
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

        mock_create_book.assert_called_once()
        mock_add_book.assert_called_once()
        current_window.destroy.assert_called_once()

    @patch("AddBook.BookFactory.create_book")
    @patch("AddBook.User.add_book_to_library")
    def test_submit_new_book_missing_fields(self, mock_add_book, mock_create_book):
        """
        Test submitting a book with missing fields.
        """
        entries = {
            "title": MagicMock(get=MagicMock(return_value="")),
            "author": MagicMock(get=MagicMock(return_value="Valid Author")),
            "copies": MagicMock(get=MagicMock(return_value="5")),
            "genre": MagicMock(get=MagicMock(return_value="Fiction")),
            "year": MagicMock(get=MagicMock(return_value="2023")),
        }
        dropdown_var = MagicMock(get=MagicMock(return_value="No"))
        current_window = MagicMock()

        with self.assertRaises(ValueError):
            submit_new_book(entries, dropdown_var, current_window, None)  # No label needed

        mock_create_book.assert_not_called()
        mock_add_book.assert_not_called()


if __name__ == "__main__":
    unittest.main()
