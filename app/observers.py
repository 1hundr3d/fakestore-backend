import logging

logger = logging.getLogger(__name__)

class Observer:
    def update(self, message: str) -> None:
        raise NotImplementedError
    
class Subject:
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

class LoggerObserver(Observer):
    def update(self, message: str) -> None:
        logger.info(message)

class EmailObserver(Observer):
    def update(self, message: str) -> None:
        print(f"[EMAIL] Отправлено: {message}")

class ProductSubject(Subject):
    pass