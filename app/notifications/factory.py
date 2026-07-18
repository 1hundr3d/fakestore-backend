class Notifier:
    def send(self, message: str) -> None:
        raise NotImplementedError
    
class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[EMAIL]: {message}")

class SMSNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[SMS]: {message}")

class NotifierFactory():
    @staticmethod
    def create_notifier(notifier_type: str) -> Notifier:
        match notifier_type:
            case 'email':
                return EmailNotifier()
            case 'sms':
                return SMSNotifier()
            case _:
                raise ValueError(f'Неизвестный тип уведомления: {notifier_type}')