from unittest.mock import patch, MagicMock
import unittest
from start.Landing import on_button_click


class TestLanding(unittest.TestCase):
    # ----------------------------------------
    # Test for on_button_click
    # ----------------------------------------
    @patch("start.Landing.main")
    @patch("start.Landing.open_login_window")
    def test_on_button_click(self, mock_open_login_window, mock_main):
        # Mock the landing window
        landing_mock = MagicMock()

        # Call the function
        on_button_click(landing_mock)

        # Assertions
        mock_main.assert_called_once()  # Ensure `main()` is called
        landing_mock.destroy.assert_called_once()  # Ensure `landing.destroy()` is called
        mock_open_login_window.assert_called_once()  # Ensure `open_login_window()` is called


if __name__ == "__main__":
    unittest.main()
