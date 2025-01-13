from abc import ABC, abstractmethod

class Subject(ABC):
    # Abstract base class for subjects in the observer pattern.
    @abstractmethod
    def add_observer(self, observer):
        # Adds an observer to the list.
        pass

    @abstractmethod
    def notify_observers(self, message, users_df):
        # Notifies all observers with a message.
        pass

    @abstractmethod
    def get_observers(self):
        # Returns the list of current observers.
        pass
