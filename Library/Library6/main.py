from FileHandler import *
import csv

def main():
    header = ["name", "password"]
    # Create the CSV file if it doesn't exist
    FileHandler.create_csv(Paths.USERS.value, header)
    FileHandler.init_loaned_books()
    FileHandler.init_available_books()


if __name__ == "__main__":
    main()
