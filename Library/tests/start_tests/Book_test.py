import unittest
from start.Book import Book


class TestBook(unittest.TestCase):
    def setUp(self):
        """Set up a shared Book instance for all tests."""
        self.book = Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            is_loaned="No",
            copies=5,
            genre="Fiction",
            year=1925
        )

    # ----------------------------------------
    # Test for book_initialization
    # ----------------------------------------
    def test_book_initialization(self):
        # Assertions for initialization
        self.assertEqual(self.book.title, "The Great Gatsby")
        self.assertEqual(self.book.author, "F. Scott Fitzgerald")
        self.assertEqual(self.book.is_loaned, "No")
        self.assertEqual(self.book.copies, 5)
        self.assertEqual(self.book.genre, "Fiction")
        self.assertEqual(self.book.year, 1925)
        self.assertEqual(self.book.copies_available, 5)
        self.assertEqual(self.book.request, 0)
        self.assertEqual(self.book.loaned_count, 0)
        self.assertEqual(self.book.waiting_list, "empty")

    # ----------------------------------------
    # Test for book_update_details
    # ----------------------------------------
    def test_book_update_details(self):
        # Update details
        self.book.update_details(
            title="1984",
            author="George Orwell",
            is_loaned="Yes",
            copies=10,
            genre="Dystopian",
            year=1949,
            request=3,
            loaned_count=5,
            waiting_list="John, Alice",
            copies_available=0
        )

        # Assertions for updated attributes
        self.assertEqual(self.book.title, "1984")
        self.assertEqual(self.book.author, "George Orwell")
        self.assertEqual(self.book.is_loaned, "Yes")
        self.assertEqual(self.book.copies, 10)
        self.assertEqual(self.book.genre, "Dystopian")
        self.assertEqual(self.book.year, 1949)
        self.assertEqual(self.book.request, 3)
        self.assertEqual(self.book.loaned_count, 5)
        self.assertEqual(self.book.waiting_list, "John, Alice")
        self.assertEqual(self.book.copies_available, 0)

    # ----------------------------------------
    # Test for book_str_representation
    # ----------------------------------------
    def test_book_str_representation(self):
        # Test string representation
        expected_str = ("Title: The Great Gatsby, Author: F. Scott Fitzgerald, Year: 1925, "
                        "Genre: Fiction, Copies: 5, Loaned: No")
        self.assertEqual(str(self.book), expected_str)


if __name__ == "__main__":
    unittest.main()
