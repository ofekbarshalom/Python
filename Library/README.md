# Library Management System - Tkinter OOP Project in Python

This project is a desktop library management system built with Python, Tkinter, and object-oriented design principles. It supports user registration/login, book management, lending/return flows, waiting lists, notifications, and CSV-based persistence.

## Files and Folders in the Project

- **`start/`**: Entry-point and initialization logic.
  - **`Landing.py`**: Landing page UI and startup flow.
  - **`main.py`**: Initializes CSV files, columns, logs, and notification system.
  - **`library.py`**: Main dashboard window with action buttons.
- **`buttons/`**: Feature windows and business actions.
  - Add/remove/search/view books
  - Lend/return books
  - Login/register pages
  - Popular books view
- **`design/`**: Core OOP design components (Observer/Subject/User/NotificationSystem).
- **`helpers/`**: Utilities for paths, CSV/file handling, logging, popup messages, and shared helpers.
- **`files/`**: Data storage files (`books.csv`, `users.csv`, `available_books.csv`, `loaned_books.csv`, `popular_books.csv`, `logs.txt`).
- **`tests/`**: Unit tests for buttons, helpers, design, and startup modules.

## Main Features

- **User Authentication**: Register and login with hashed passwords.
- **Book Management**: Add, remove, search, and view books.
- **Lending System**: Lend and return books with updates to availability and loaned lists.
- **Waiting List Support**: Queue users when books are unavailable.
- **Popular Books Tracking**: Maintains top books based on requests/loan count.
- **Notifications**: Observer-based notification logic for users.
- **CSV Persistence**: All data is stored locally in CSV files.
- **Logging**: Action and error logs written to `files/logs.txt`.

## Requirements

- Python 3.10 or higher
- `pandas`
- `tkinter`

Install dependencies:

```bash
pip install pandas
```

## Running the Program

Run from the project root (`Library/`):

### 1. Start the Application

```bash
python start/Landing.py
```

This opens the landing page and initializes required project files/columns on first use.

### 2. Use the App

From the UI flow:

1. Click **Get Started** on the landing page.
2. Login or register a user.
3. Open the library dashboard.
4. Use buttons to add/search/lend/return/remove books and view popular books.

## Running Tests

Run all tests from the project root:

```bash
python -m unittest discover -s tests
```

## Additional Notes

- Paths are managed centrally in `helpers/path.py` and are relative to project location.
- Missing CSV files are created automatically during initialization.
- This project is designed for educational use and demonstrates practical OOP patterns in a GUI app.

## Authors

This project was developed as part of an OOP university assignment.

## License

This project is for educational purposes.