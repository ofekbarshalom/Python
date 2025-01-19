import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from design.NotificationSystem import NotificationSystem
from helpers.path import Paths


class TestNotificationSystem(unittest.TestCase):
    def setUp(self):
        # Set up the singleton instance and mock observers for testing.
        self.notification_system = NotificationSystem.get_instance()
        self.notification_system._observers = []  # Ensure clean state

        # Mock observers
        self.mock_observer_1 = MagicMock()
        self.mock_observer_1.name = "Observer1"

        self.mock_observer_2 = MagicMock()
        self.mock_observer_2.name = "Observer2"

        # Mock user DataFrame
        self.mock_users_df = pd.DataFrame({
            "name": ["Observer1", "Observer2"],
            "messages": ["empty", "empty"]
        })

    # ----------------------------------------
    # Test for get_instance
    # ----------------------------------------
    def test_get_instance(self):
        # Ensure the NotificationSystem is a singleton.
        another_instance = NotificationSystem.get_instance()
        self.assertIs(self.notification_system, another_instance, "NotificationSystem is not a singleton.")

    # ----------------------------------------
    # Test for add_observer
    # ----------------------------------------
    def test_add_observer(self):
        # Test adding observers to the notification system.
        self.notification_system.add_observer(self.mock_observer_1)
        self.assertIn(self.mock_observer_1, self.notification_system.get_observers(), "Observer1 was not added.")

        # Add the same observer again and check for duplicates.
        self.notification_system.add_observer(self.mock_observer_1)
        self.assertEqual(len(self.notification_system.get_observers()), 1, "Duplicate observers were added.")

    # ----------------------------------------
    # Test for notify_observers
    # ----------------------------------------
    def test_notify_observers(self):
        # Test notifying observers with a message and updating the DataFrame.
        self.notification_system.add_observer(self.mock_observer_1)
        self.notification_system.add_observer(self.mock_observer_2)

        # Call notify_observers.
        self.notification_system.notify_observers("Test message", self.mock_users_df)

        # Assert each observer's update method was called.
        self.mock_observer_1.update.assert_called_once_with("Test message", self.mock_users_df)
        self.mock_observer_2.update.assert_called_once_with("Test message", self.mock_users_df)

    @patch("design.NotificationSystem.pd.DataFrame.to_csv")
    def test_notify_observers_csv_save(self, mock_to_csv):
        # Test that the updated DataFrame is saved to a CSV after notifying observers.
        self.notification_system.add_observer(self.mock_observer_1)
        self.notification_system.notify_observers("Test message", self.mock_users_df)

        # Assert the DataFrame was saved to a CSV.
        mock_to_csv.assert_called_once_with(Paths.USERS.value, index=False)

    # ----------------------------------------
    # Test for get_observers
    # ----------------------------------------
    def test_get_observers(self):
        # Test retrieving the list of observers.
        self.notification_system.add_observer(self.mock_observer_1)
        self.notification_system.add_observer(self.mock_observer_2)

        observers = self.notification_system.get_observers()
        self.assertEqual(len(observers), 2, "Number of observers retrieved is incorrect.")
        self.assertIn(self.mock_observer_1, observers, "Observer1 is missing in the retrieved list.")
        self.assertIn(self.mock_observer_2, observers, "Observer2 is missing in the retrieved list.")


if __name__ == "__main__":
    unittest.main()
