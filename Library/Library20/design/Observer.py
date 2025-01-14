from abc import ABC, abstractmethod

class Observer(ABC):
    # Abstract base class for observers in the observer pattern.

    @abstractmethod
    def update(self, message, users_df):
        # Receives a message from the subject.
        pass
