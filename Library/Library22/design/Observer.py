from abc import ABC, abstractmethod

class Observer(ABC):
    """
        Abstract base class for observers in the Observer design pattern.
        Classes implementing this interface should define the 'update' method
        to handle notifications from the subject.
    """
    # Abstract base class for observers in the observer pattern.

    @abstractmethod
    def update(self, message, users_df):
        """
            Receive a notification message from the subject.
            :param message: The notification message sent by the subject.
            :param users_df: A DataFrame containing the users' data to be updated.
        """
        # Receives a message from the subject.
        pass
