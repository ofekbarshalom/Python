import unittest
from unittest.mock import patch, MagicMock, call
import logging
from helpers.path import Paths
from helpers.logger import Logger


class TestLogger(unittest.TestCase):

    @patch("helpers.logger.logging.getLogger")  # Mock the logging module's getLogger
    @patch("helpers.logger.logging.FileHandler")  # Mock FileHandler to avoid file I/O
    def test_get_logger_initialization(self, mock_file_handler, mock_get_logger):
        # Mock the logger instance
        mock_logger_instance = MagicMock()
        mock_get_logger.return_value = mock_logger_instance
        mock_file_handler_instance = MagicMock()
        mock_file_handler.return_value = mock_file_handler_instance

        # Call the method
        logger = Logger.get_logger()

        # Assertions
        mock_get_logger.assert_called_once_with("SystemLogger")
        mock_logger_instance.setLevel.assert_called_once_with(logging.DEBUG)
        mock_file_handler.assert_called_once_with(Paths.LOGGER.value)
        mock_file_handler_instance.setLevel.assert_called_once_with(logging.DEBUG)
        mock_logger_instance.addHandler.assert_called_once_with(mock_file_handler_instance)
        self.assertEqual(logger, mock_logger_instance)

    @patch("helpers.logger.Logger.get_logger")
    def test_log_decorator_success(self, mock_get_logger):
        # Mock the logger instance
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Decorated function
        @Logger.log_decorator("Success message", "Failure message")
        def sample_function():
            return "Success"

        # Call the function
        result = sample_function()

        # Assertions
        self.assertEqual(result, "Success")
        mock_logger.info.assert_called_once_with("Success message")
        mock_logger.error.assert_not_called()

    @patch("helpers.logger.Logger.get_logger")
    def test_log_decorator_failure(self, mock_get_logger):
        # Mock the logger instance
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Decorated function
        @Logger.log_decorator("Success message", "Failure message")
        def sample_function():
            raise Exception("Simulated failure")

        # Call the function
        result = sample_function()

        # Assertions
        self.assertIsNone(result)
        mock_logger.error.assert_called_once_with("Failure message")
        mock_logger.info.assert_not_called()

    @patch("helpers.logger.Logger.get_logger")
    def test_log_search_success(self, mock_get_logger):
        # Mock the logger instance
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Mock objects
        search_entry = MagicMock()
        search_entry.get.return_value = "Book A"
        search_type_combobox = MagicMock()
        search_type_combobox.get.return_value = "Title"
        table = MagicMock()

        # Decorated function
        @Logger.log_search()
        def sample_search_function(search_entry, search_type_combobox, table):
            return "Search Success"

        # Call the function
        result = sample_search_function(search_entry, search_type_combobox, table)

        # Assertions
        self.assertEqual(result, "Search Success")
        mock_logger.info.assert_called_once_with("Search book 'Book A' by Title completed successfully")
        mock_logger.error.assert_not_called()

    @patch("helpers.logger.Logger.get_logger")
    def test_log_search_failure(self, mock_get_logger):
        # Mock the logger instance
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Mock objects
        search_entry = MagicMock()
        search_entry.get.return_value = "Book A"
        search_type_combobox = MagicMock()
        search_type_combobox.get.return_value = "Title"
        table = MagicMock()

        # Decorated function
        @Logger.log_search()
        def sample_search_function(search_entry, search_type_combobox, table):
            raise Exception("Simulated failure")

        # Call the function and expect an exception
        with self.assertRaises(Exception):
            sample_search_function(search_entry, search_type_combobox, table)

        # Assertions
        mock_logger.error.assert_called_once_with("Search book 'Book A' by Title completed fail")
        mock_logger.info.assert_not_called()

    @patch("helpers.logger.Logger.get_logger")
    def test_log_with_param_success(self, mock_get_logger):
        # Mock the logger instance
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Decorated function
        @Logger.log_with_param("Action with {0} succeeded", "Action with {0} failed")
        def sample_function(param=None):
            return "Success"

        # Call the function
        result = sample_function(param="TestParam")

        # Assertions
        self.assertEqual(result, "Success")
        mock_logger.info.assert_called_once_with("Action with TestParam succeeded")
        mock_logger.error.assert_not_called()

    @patch("helpers.logger.Logger.get_logger")
    def test_log_with_param_failure(self, mock_get_logger):
        # Mock the logger instance
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Decorated function
        @Logger.log_with_param("Action with {0} succeeded", "Action with {0} failed")
        def sample_function(param=None):
            raise Exception("Simulated failure")

        # Call the function and expect an exception
        with self.assertRaises(Exception):
            sample_function(param="TestParam")

        # Assertions
        mock_logger.error.assert_called_once_with("Action with TestParam failed")
        mock_logger.info.assert_not_called()


if __name__ == "__main__":
    unittest.main()
