from Subject import Subject
import pandas as pd
from path import Paths

class NotificationSystem(Subject):

    _instance = None

    def __init__(self):
        self._observers = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_observer(self, observer):
        if observer not in self._observers:
            print(f"Adding observer: {observer.name}")
            self._observers.append(observer)

    def notify_observers(self, message, users_df):
        for observer in self._observers:
            print(f"Notifying observer: {observer.name}")
            observer.update(message, users_df)

        # Save the updated DataFrame back to the CSV
        try:
            users_df.to_csv(Paths.USERS.value, index=False)
            print("CSV saved successfully.")
        except Exception as e:
            print(f"Failed to save CSV: {e}")

    def get_observers(self):
        return self._observers
