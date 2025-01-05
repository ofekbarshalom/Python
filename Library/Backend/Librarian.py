from Book import Book  # Import the Book class
from User import *

class Librarian(User):
    def __init__(self, name, password, is_librarian=True):
       super().__init__(name, password, is_librarian)

    @staticmethod
    def add_book_to_library(book, file_path="books.csv"):
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write a row with book details
            writer.writerow([book.title, book.author, book.is_loaned, book.copies, book.genre, book.year])

    @staticmethod
    def delete_book_from_library(book_title, file_path="books.csv"):
        books = []
        book_found = False

        # Read the current contents of the file
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header row
            books.append(header)

            # Process the remaining rows
            for row in reader:
                if row[0] == book_title:  # If the book title matches, skip this row
                    book_found = True
                else:
                    books.append(row)

        # Write the updated contents back to the same file
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(books)

        if book_found:
            print(f"The book '{book_title}' has been successfully deleted.")
        else:
            print(f"The book '{book_title}' was not found in the library.")

    @staticmethod
    def update_book_in_library(book_title, file_path="books.csv"):
        books = []
        book_found = False

        # Read the current contents of the file
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header row
            books.append(header)

            for row in reader:
                if row[0] == book_title:  # If the book title matches, skip this row
                    book_found = True
                    # Replace the row with the updated details from the book object
                    updated_row = [book.title,book.author,book.is_loaned,book.copies,book.genre,book.year]
                    books.append(updated_row)
                else:
                    books.append(row)

        # Write the updated contents back to the same file
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(books)

        if book_found:
            print(f"The book '{book_title}' has been successfully updated.")
        else:
            print(f"The book '{book_title}' was not found in the library.")