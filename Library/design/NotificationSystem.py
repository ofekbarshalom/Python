from design.Subject import Subject
from helpers.path import Paths
import pandas as pd

class NotificationSystem(Subject):
    """
       Singleton class for managing and notifying observers in the library system.
       Inherits from the Subject base class.
    """

    _instance = None

    def __init__(self):
        """
            Initialize the NotificationSystem with an empty list of observers.
        """
        self._observers = []

    @classmethod
    def get_instance(cls):
        """
            Retrieve the singleton instance of the NotificationSystem.
            Creates the instance if it does not already exist.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_observer(self, observer):
        """
            Add a new observer to the list if not already present.
            :param observer: An instance of a class implementing the Observer interface.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def notify_observers(self, message, users_df):
        """
            Notify all observers with a given message.
            :param message: The notification message to send to observers.
            :param users_df: The DataFrame containing user data to update.
        """
        for observer in self._observers:
            observer.update(message, users_df)

        # Save the updated DataFrame back to the CSV
        try:
            users_df.to_csv(Paths.USERS.value, index=False)
        except Exception as e:
            print(f"Failed to save CSV: {e}")

    def get_observers(self):
        """
            Retrieve the list of registered observers.
            :return: List of observers.
        """
        return self._observers
