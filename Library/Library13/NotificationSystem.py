from Subject import Subject

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
        for observer in self._observers:
            observer.update(message)

    def get_observers(self):
        return self._observers
