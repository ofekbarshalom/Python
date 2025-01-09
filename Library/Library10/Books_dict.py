from FileHandler import FileHandler
from Book import Book
from queue import Queue

books_dict = {}

def initialize_books_dict():
    global books_dict
    books_dict = FileHandler.create_books_dict_from_csv()  # Initialize using FileHandler
    print("Global books_dict has been initialized.")

def add_book_to_dict(book):
    if book.title in books_dict:
        print(f"Book '{book.title}' already exists in the dictionary.")
        return
    books_dict[book.title] = book
    print(f"Book '{book.title}' added to the dictionary.")

def remove_book_from_dict(book_title):
    if book_title in books_dict:
        del books_dict[book_title]
        print(f"Book '{book_title}' removed from the dictionary.")
        return
    print(f"Book '{book_title}' not found in the dictionary.")

def get_book_object(book_title):
    if book_title in books_dict:
        return books_dict[book_title]
    else:
        print(f"Book '{book_title}' not found in the dictionary.")
        return None

def update_book_waiting_list(book_title, client_name):
    if book_title in books_dict:
        # Retrieve the book object
        book = books_dict[book_title]

        # Add the client to the book's queue
        book.client_queue.put(client_name)
        book.request += 1

        # Print confirmation message
        print(f"Client '{client_name}' added to the waiting list of book '{book_title}'.")
        return True

    # Book not found in the dictionary
    print(f"Book '{book_title}' not found in the dictionary.")
    return False


