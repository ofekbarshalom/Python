from Subject import Subject
from FileHandler import FileHandler

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

    def notify_observers(self, message):
        users_df = FileHandler.read_users_file()

        for observer in self._observers:
            observer.update(message, users_df)

        # Save the updated DataFrame back to the CSV
        users_df.to_csv(Paths.USERS.value, index=False)
        print(f"Observers notified and messages updated in {Paths.USERS.value}.")

    def get_observers(self):
        return self._observers
