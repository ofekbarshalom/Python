import os
from enum import Enum

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Paths(Enum):
    USERS = os.path.join(BASE_DIR, "files", "users.csv")
    BOOKS = os.path.join(BASE_DIR, "files", "books.csv")
    AVAILABLE_BOOKS = os.path.join(BASE_DIR, "files", "available_books.csv")
    LOANED_BOOKS = os.path.join(BASE_DIR, "files", "loaned_books.csv")
    POPULAR_BOOKS = os.path.join(BASE_DIR, "files", "popular_books.csv")
    LOGGER = os.path.join(BASE_DIR, "files", "logs.txt")
