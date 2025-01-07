import csv
import hashlib
from Book import Book
from path import Paths

class FileHandler:
    @staticmethod
    def create_books_dict_from_csv(file_path=Paths.BOOKS.value):
        books_dict = {}  # Initialize an empty dictionary

        # Open the CSV file for reading
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # Use DictReader for column-based access

            # Process each row in the CSV
            for row in reader:
                title = row['title']  # Extract the title for the dictionary key
                author = row['author']
                is_loaned = row['is_loaned'].lower() == "yes"  # Convert "Yes" or "No" to boolean
                copies = int(row['copies'])
                genre = row['genre']
                year = int(row['year'])  # Directly convert year to an integer

                # Create a Book object using BookFactory
                book = BookFactory.create_book(title, author, is_loaned, copies, genre, year)

                # Add the Book object to the dictionary with title as the key
                books_dict[title] = book

        return books_dict

    @staticmethod
    def create_csv(file_path, headers=None):
        if headers is None or not isinstance(headers, list):
            raise ValueError("Headers must be provided as a list of column names.")

        # Open the file in append mode and check if it's empty
        with open(file_path, mode='a+', newline='', encoding='utf-8') as file:
            file.seek(0)
            reader = csv.reader(file)
            first_row = next(reader, None)  # Read the first row or None if empty

            # If the file is empty or doesn't contain headers, write them
            if not first_row:
                writer = csv.writer(file)
                writer.writerow(headers)
                print(f"Headers added to '{file_path}': {headers}")
            else:
                print(f"Headers already exist in '{file_path}'.")

    @staticmethod
    def remove_book_from_csv(book_title, file_path=Paths.BOOKS.value):
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
            print(f"The book '{book_title}' was not found in the csv.")

    @staticmethod
    def update_book_in_csv(file_path, book_title, column_name, new_info):
        books = []
        book_found = False

        # Read the current contents of the file
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header row
            books.append(header)

            # Ensure the column name exists in the header
            if column_name not in header:
                raise ValueError(f"Column '{column_name}' not found in the CSV file.")

            # Get the index of the column to be updated
            column_index = header.index(column_name)

            # Process the remaining rows
            for row in reader:
                if row[0] == book_title:  # If the book title matches
                    book_found = True
                    row[column_index] = new_info  # Update the specified column with new information
                books.append(row)

        # Write the updated contents back to the same file
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(books)

        if book_found:
            print(f"The book '{book_title}' has been successfully updated.")
        else:
            print(f"The book '{book_title}' was not found in the CSV.")

    @staticmethod
    def init_available_books(books_file_path=Paths.BOOKS.value, available_books_file_path=Paths.AVAILABLE_BOOKS.value):
        header = ['title', 'copies_available']
        FileHandler.create_csv(available_books_file_path, header)  # Ensure loaned_books.csv exists with correct headers

        try:
            # Open the books file for reading
            with open(books_file_path, mode='r', newline='', encoding='utf-8') as books_file:
                reader = csv.DictReader(books_file)

                # Open the loaned books file for appending
                with open(available_books_file_path, mode='a', newline='', encoding='utf-8') as loaned_books_file:
                    writer = csv.writer(loaned_books_file)

                    # Process each row in books.csv
                    for row in reader:
                        title = row['title']
                        copies_available = int(row['copies_available'])

                        # If loaned copies > 0, write to loaned_books.csv
                        if copies_available > 0:
                            writer.writerow([title, copies_available])

            print(f"The file '{available_books_file_path}' has been successfully updated with loaned books.")

        except FileNotFoundError:
            print(f"The file '{books_file_path}' does not exist.")

    @staticmethod
    def init_loaned_books(books_file_path=Paths.BOOKS.value, loaned_books_file_path=Paths.LOANED_BOOKS.value):
        header = ['title']
        FileHandler.create_csv(loaned_books_file_path, header)  # Ensure loaned_books.csv exists with correct headers

        try:
            # Open the books file for reading
            with open(books_file_path, mode='r', newline='', encoding='utf-8') as books_file:
                reader = csv.DictReader(books_file)

                # Open the loaned books file for appending
                with open(loaned_books_file_path, mode='a', newline='', encoding='utf-8') as loaned_books_file:
                    writer = csv.writer(loaned_books_file)

                    # Process each row in books.csv
                    for row in reader:
                        title = row['title']
                        is_loaned = row['is_loaned']

                        if is_loaned == "Yes":
                            writer.writerow([title])

            print(f"The file '{loaned_books_file_path}' has been successfully updated with loaned books.")

        except FileNotFoundError:
            print(f"The file '{books_file_path}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def check_login(name, password, file_path=Paths.USERS.value):
        try:
            # Open the CSV file for reading
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Check each row for the username
                for row in reader:
                    if row["name"] == name:  # Username found
                        hashed_password = FileHandler.hash_password(password)
                        if row["password"] == hashed_password:  # Check if passwords match
                            return True  # Username and password are correct
                        else:
                            print("Password is incorrect")
                            return False  # Incorrect password

                print("Username is incorrect")
                return False  # Username not found

        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        except Exception as e:
            raise Exception(f"An error occurred while checking the username: {e}")

    @staticmethod
    def hash_password(password):
        # Create an SHA-256 hash object
        hash_object = hashlib.sha256()

        # Encode the password to bytes, then hash it
        hash_object.update(password.encode('utf-8'))

        # Get the hexadecimal representation of the hash
        return hash_object.hexdigest()

    @staticmethod
    def check_name(name, file_path=Paths.USERS.value):
        try:
            # Open the CSV file for reading
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Check each row for the username
                for row in reader:
                    if row["name"] == name:  # Username found
                        return True
                return False

        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        except Exception as e:
            raise Exception(f"An error occurred while checking the username: {e}")
