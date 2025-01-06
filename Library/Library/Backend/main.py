from Book import Book  # Import the Book class
from Librarian import *
import csv


def main():
    # Create the CSV file if it doesn't exist
    create_csv(file_path="users.csv")

    # Create Book objects
    book1 = Book(title="1984", author="George Orwell", is_loaned=False, copies=1, genre="Dystopian", year=1949)
    book2 = Book(title="Brave New World", author="Aldous Huxley", is_loaned=False, copies=1, genre="Science Fiction",year=1932)
    book3 = Book(title="Pride and Prejudice", author="Jane Austen", is_loaned=False, copies=1, genre="Romance",year=1813)
    book4 = Book(title="Infi 1", author="R. wiess", is_loaned=False, copies=2, genre="Shit",year=2010)

    # Create users
    librarian1 = Librarian(name="Bob", password="securepassword789")

    # Print the contents of the CSV file
    print("\nContents of 'users.csv' after adding users:")
    with open("users.csv", mode="r", encoding="utf-8") as file:
        print(file.read())

    if Librarian.check_login("Bob", "securepassword789"):
        print("YEH!")
    else:
        print("semek")

    #librarian1.add_book_to_library(book4)
    #librarian1.delete_book_from_library(book4)
    #book4.update_details(author="gay")
    #librarian1.update_book_in_library(book4)

    # Print the contents of the CSV file after updates
    # print("\nContents of 'books.csv' after updates:")
    # with open("books.csv", mode="r", encoding="utf-8") as file:
    #     print(file.read())


if __name__ == "__main__":
    main()
