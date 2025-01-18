import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
import pandas as pd
from buttons.login import *

class TestLoginFunctions(unittest.TestCase):
    # ----------------------------------------
    # Test for submit_login
    # ----------------------------------------
    @patch("buttons.login.open_library_window")  # Mock the library opening function
    @patch("buttons.login.MessagesPopUp.show_messages_pop_up")  # Mock the messages pop-up
    @patch("buttons.login.FileHandler.check_login")  # Mock the login check function
    @patch("buttons.login.Logger.get_logger")  # Mock the logger
    def test_submit_login(self, mock_get_logger, mock_check_login, mock_show_messages, mock_open_library):
        # Mock the logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Mock successful login
        mock_check_login.return_value = True

        # Create tkinter objects
        current_window = MagicMock()  # Mock the Tkinter window
        current_window.after = MagicMock(side_effect=lambda delay, func: func())  # Call the function immediately

        username_entry = MagicMock(get=MagicMock(return_value="valid_user"))
        password_entry = MagicMock(get=MagicMock(return_value="valid_password"))

        # Call the function
        submit_login(username_entry, password_entry, current_window)

        # Assertions
        mock_check_login.assert_called_once_with("valid_user", "valid_password")
        mock_show_messages.assert_called_once_with("valid_user")
        mock_open_library.assert_called_once()
        mock_logger.info.assert_called_with("logged in successfully")

        # Ensure current_window.destroy was called
        current_window.destroy.assert_called_once()


if __name__ == "__main__":
    unittest.main()
