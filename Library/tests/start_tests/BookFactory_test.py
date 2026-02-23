import unittest
from start.Book import Book
from start.BookFactory import BookFactory

class TestBookFactory(unittest.TestCase):
    def test_create_book_valid(self):
        # Test creating a valid book
        book = BookFactory.create_book(
            title="1984",
            author="George Orwell",
            is_loaned=False,
            copies=5,
            genre="Dystopian",
            year=1949
        )
        self.assertIsInstance(book, Book)
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "George Orwell")
        self.assertFalse(book.is_loaned)
        self.assertEqual(book.copies, 5)
        self.assertEqual(book.genre, "Dystopian")
        self.assertEqual(book.year, 1949)

    def test_create_book_missing_title(self):
        # Test missing title raises ValueError
        with self.assertRaises(ValueError) as context:
            BookFactory.create_book(
                title="",
                author="George Orwell",
                is_loaned=False,
                copies=5,
                genre="Dystopian",
                year=1949
            )
        self.assertEqual(str(context.exception), "Title and author are required to create a book.")

    def test_create_book_negative_copies(self):
        # Test negative copies raises ValueError
        with self.assertRaises(ValueError) as context:
            BookFactory.create_book(
                title="1984",
                author="George Orwell",
                is_loaned=False,
                copies=-1,
                genre="Dystopian",
                year=1949
            )
        self.assertEqual(str(context.exception), "Number of copies cannot be negative.")


if __name__ == "__main__":
    unittest.main()
