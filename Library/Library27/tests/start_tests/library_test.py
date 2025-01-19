import unittest
from unittest.mock import patch, MagicMock
from start.library import open_library_window
import tkinter as tk


class TestLibrary(unittest.TestCase):
    @patch("start.library.tk.Tk")
    @patch("start.library.tk.Label")
    @patch("start.library.tk.Frame")
    @patch("start.library.tk.Button")
    @patch("start.library.utils.center_window")
    def test_open_library_window(self, mock_center_window, mock_button, mock_frame, mock_label, mock_tk):
        # Mock the root Tkinter window
        root_mock = MagicMock()
        mock_tk.return_value = root_mock

        # Mock other widgets
        frame_mock = MagicMock()
        mock_frame.return_value = frame_mock

        label_mock = MagicMock()
        mock_label.return_value = label_mock

        button_mock = MagicMock()
        mock_button.return_value = button_mock

        # Call the function being tested
        open_library_window()

        # Assertions for the main window
        mock_tk.assert_called_once()  # Ensure Tk() is called
        root_mock.title.assert_called_once_with("Library")  # Check title
        root_mock.configure.assert_called_once_with(bg="#f2f2f2")  # Check background color
        mock_center_window.assert_called_once_with(root_mock, 1000, 300)  # Ensure window is centered
        root_mock.mainloop.assert_called_once()  # Ensure mainloop is called

        # Check if header is created
        mock_label.assert_any_call(
            root_mock,
            text="Library",
            font=("Arial", 24, "bold"),
            bg="#4b0082",
            fg="white",
        )
        label_mock.pack.assert_called_once_with(fill=tk.X, pady=(0, 10))

        # Check if the buttons frame is created
        mock_frame.assert_any_call(root_mock, bg="#f2f2f2")
        frame_mock.pack.assert_called_once_with(pady=(20, 20), expand=True)

        # Check if buttons are created
        buttons = ["Add Book","Remove Book","Search Book","View Books","Lend Book","Return Book","Logout","Login","Register","Popular Books"]
        for button_text in buttons:
            mock_button.assert_any_call(
                frame_mock,
                text=button_text,
                font=("Arial", 12, "bold"),
                bg="#4b0082",
                fg="white",
                width=15,
                command=unittest.mock.ANY,
            )

        # Ensure buttons are placed in the grid
        expected_grid_calls = []
        for idx in range(len(buttons)):
            row = idx // 5  # 5 buttons per row
            col = idx % 5
            expected_grid_calls.append(
                unittest.mock.call(row=row, column=col, padx=10, pady=10)
            )
        button_mock.grid.assert_has_calls(expected_grid_calls, any_order=False)


if __name__ == "__main__":
    unittest.main()
