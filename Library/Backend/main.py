from User import User  # Import the User class
from Book import Book  # Import the Book class
from Librarian import *
from UserFactory import *


def main():
    # Create the CSV file if it doesn't exist
    User.create_csv(file_path="users.csv")

    # Create Book objects
    book1 = Book(title="1984", author="George Orwell", is_loaned=False, copies=1, genre="Dystopian", year=1949)
    book2 = Book(title="Brave New World", author="Aldous Huxley", is_loaned=False, copies=1, genre="Science Fiction",year=1932)
    book3 = Book(title="Pride and Prejudice", author="Jane Austen", is_loaned=False, copies=1, genre="Romance",year=1813)
    book4 = Book(title="Infi 1", author="R. wiess", is_loaned=False, copies=2, genre="Shit",year=2010)

    # Create users
    user1 = UserFactory.create_user(name="Alice", password="mypassword123", is_librarian=False, borrowed_books=[book1, book2])
    librarian1 = UserFactory.create_user(name="Bob", password="securepassword789", is_librarian=True)

    # print("Initial users added to the CSV file.")

    # Print the contents of the CSV file
    # print("\nContents of 'users.csv' after adding users:")
    # with open("users.csv", mode="r", encoding="utf-8") as file:
    #     print(file.read())

    #librarian1.add_book_to_library(book4)
    #librarian1.delete_book_from_library(book4)
    book4.update_details(author="gay")
    librarian1.update_book_in_library(book4)

    # Print the contents of the CSV file after updates
    # print("\nContents of 'books.csv' after updates:")
    # with open("books.csv", mode="r", encoding="utf-8") as file:
    #     print(file.read())


if __name__ == "__main__":
    main()
