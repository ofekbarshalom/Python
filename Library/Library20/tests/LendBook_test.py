import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from your_module import update_loaned_count

class TestBookLending(unittest.TestCase):

    def test_update_loaned_count_invalid_book(self):
        books_df = pd.DataFrame({
            "title": ["Book A", "Book B"],
            "loaned_count": [3, 5],
            "waiting_list": ["Alice,Bob", "empty"]
        })

        # Call the method
        result = update_loaned_count("Book C", books_df)

        # Assertions
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
