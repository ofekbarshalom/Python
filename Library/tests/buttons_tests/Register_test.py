import unittest
from unittest.mock import patch, MagicMock, call
from buttons.register import submit_register


class TestRegister(unittest.TestCase):
    # ----------------------------------------
    # Test for submit_register when fields are missing
    # ----------------------------------------
    @patch("buttons.register.Logger.get_logger")  # Mock the logger
    def test_submit_register_missing_fields(self, mock_get_logger):
        # Mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Mock Tkinter components
        current_window = MagicMock()
        current_window.after = MagicMock(side_effect=lambda delay, func: func())  # Immediate callback
        name_entry = MagicMock(get=MagicMock(return_value=""))  # Missing username
        password_entry = MagicMock(get=MagicMock(return_value=""))  # Missing password
        alert_label = MagicMock()

        # Call function
        submit_register(name_entry, password_entry, current_window, alert_label)

        # Assertions for both calls
        alert_label.config.assert_has_calls([
            call(text="Name and Password are required!", fg="red"),
            call(text="")  # Clear the message
        ])
        mock_logger.error.assert_called_once_with("registered fail")
        current_window.destroy.assert_not_called()  # Window should not close

    # ----------------------------------------
    # Test for submit_register when the name already exists
    # ----------------------------------------
    @patch("buttons.register.FileHandler.check_name")  # Mock the name check function
    @patch("buttons.register.Logger.get_logger")  # Mock the logger
    def test_submit_register_name_exists(self, mock_get_logger, mock_check_name):
        # Mock logger and check_name
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_check_name.return_value = True  # Username exists

        # Mock Tkinter components
        current_window = MagicMock()
        current_window.after = MagicMock(side_effect=lambda delay, func: func())  # Immediate callback
        name_entry = MagicMock(get=MagicMock(return_value="existing_user"))
        password_entry = MagicMock(get=MagicMock(return_value="password"))
        alert_label = MagicMock()

        # Call function
        submit_register(name_entry, password_entry, current_window, alert_label)

        # Assertions for both calls
        alert_label.config.assert_has_calls([
            call(text="Name already exists!", fg="red"),
            call(text="")  # Clear the message
        ])
        mock_logger.error.assert_called_once_with("registered fail")
        current_window.destroy.assert_not_called()  # Window should not close

    # ----------------------------------------
    # Test for submit_register when everything is valid
    # ----------------------------------------
    @patch("buttons.login.open_login_window")  # Patch where the function is defined
    @patch("buttons.register.NotificationSystem.get_instance")  # Mock the Notification System
    @patch("buttons.register.FileHandler.check_name")  # Mock the name check function
    @patch("buttons.register.Logger.get_logger")  # Mock the logger
    @patch("buttons.register.User")  # Mock the User class
    def test_submit_register_success(self, mock_user, mock_get_logger, mock_check_name, mock_notification_system,
                                     mock_open_login):
        # Mock logger and check_name
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_check_name.return_value = False  # Username doesn't exist

        # Mock Notification System
        mock_notification_system_instance = MagicMock()
        mock_notification_system.return_value = mock_notification_system_instance

        # Mock User creation
        mock_new_user = MagicMock()
        mock_user.return_value = mock_new_user

        # Mock Tkinter components
        current_window = MagicMock()
        current_window.after = MagicMock(side_effect=lambda delay, func: func())  # Immediate callback
        name_entry = MagicMock(get=MagicMock(return_value="new_user"))
        password_entry = MagicMock(get=MagicMock(return_value="password"))
        alert_label = MagicMock()

        # Call function
        submit_register(name_entry, password_entry, current_window, alert_label)

        # Assertions
        mock_check_name.assert_called_once_with("new_user")
        mock_user.assert_called_once_with("new_user", "password")  # User should be created
        mock_notification_system_instance.add_observer.assert_called_once_with(mock_new_user)  # User added as observer
        mock_open_login.assert_called_once()
        mock_logger.info.assert_called_once_with("registered successfully")
        current_window.destroy.assert_called_once()  # Window should close


if __name__ == "__main__":
    unittest.main()
