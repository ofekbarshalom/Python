from abc import ABC, abstractmethod

class Subject(ABC):
    """
        Abstract base class for subjects in the Observer design pattern.
        Subjects maintain a list of observers and provide methods for managing and notifying them.
    """
    # Abstract base class for subjects in the observer pattern.
    @abstractmethod
    def add_observer(self, observer):
        """
            Add an observer to the subject.
            :param observer: An instance of a class implementing the Observer interface.
        """
        # Adds an observer to the list.
        pass

    @abstractmethod
    def notify_observers(self, message, users_df):
        """
            Notify all registered observers with a message and updated user data.
            :param message: The notification message to be sent to observers.
            :param users_df: A DataFrame containing the users' data to be updated.
        """
        # Notifies all observers with a message.
        pass

    @abstractmethod
    def get_observers(self):
        """
            Retrieve the list of currently registered observers.
            :return: A list of observers.
        """
        # Returns the list of current observers.
        pass
