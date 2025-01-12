from abc import ABC, abstractmethod

class Observer(ABC):
    # Abstract base class for observers in the observer pattern.

    @abstractmethod
    def update(self, message):
        # Receives a message from the subject.
        pass

    @abstractmethod
    def clear_messages(self):
        # Clear the messages the user already read
        pass
