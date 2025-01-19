import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from buttons.ViewBooks import update_table_with_pandas


class TestViewBooks(unittest.TestCase):
    # ----------------------------------------
    # Tests for update_table_with_pandas
    # ----------------------------------------
    @patch("buttons.ViewBooks.load_books_from_file")
    def test_update_table_with_pandas_valid_file(self, mock_load_books_from_file):
        # Mock the DataFrame returned by load_books_from_file
        df = pd.DataFrame({
            "title": ["Book A", "Book B"],
            "author": ["Author A", "Author B"],
            "year": [2020, 2018]
        })
        mock_load_books_from_file.return_value = df

        # Mock the table with a simulated state
        table_state = {"columns": []}
        table = MagicMock()
        table.__getitem__.side_effect = lambda key: table_state[key]
        table.__setitem__.side_effect = lambda key, value: table_state.update({key: value})

        # Call the function
        update_table_with_pandas(table, "mock_file.csv")

        # Assertions
        self.assertEqual(table["columns"], list(df.columns))  # Check that columns are set correctly

        # Check that headings and columns are created
        for col in df.columns:
            table.heading.assert_any_call(col, text=col)
            table.column.assert_any_call(col, width=150)

        # Check that rows are inserted
        expected_calls = [
            (("", "end"), {"values": ["Book A", "Author A", 2020]}),
            (("", "end"), {"values": ["Book B", "Author B", 2018]}),
        ]
        table.insert.assert_has_calls([unittest.mock.call(*args, **kwargs) for args, kwargs in expected_calls],any_order=False)

    @patch("buttons.ViewBooks.load_books_from_file")
    def test_update_table_with_pandas_file_not_found(self, mock_load_books_from_file):
        # Mock load_books_from_file to return None (file not found)
        mock_load_books_from_file.return_value = None

        # Mock the table with a simulated state
        table_state = {"columns": []}
        table = MagicMock()
        table.__getitem__.side_effect = lambda key: table_state[key]
        table.__setitem__.side_effect = lambda key, value: table_state.update({key: value})

        # Call the function
        update_table_with_pandas(table, "nonexistent_file.csv")

        # Assertions
        self.assertEqual(table["columns"], ("Error",))  # Check that error column is set
        table.heading.assert_called_once_with("Error", text="Error")
        table.column.assert_called_once_with("Error", width=200)
        table.insert.assert_called_once_with("", "end", values=("Error: File not found or empty!",))


if __name__ == "__main__":
    unittest.main()
