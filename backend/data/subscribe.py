import logging
import re

from .database import DETA

logging.basicConfig(level=logging.DEBUG)


class Subscription(DETA):

    def __init__(self, email: str = '', is_subscribed: bool = True) -> None:
        if not email == '':
            if not self._validate_email(email):
                raise ValueError("Invalid email address")
            self.key = email
            self.is_subscribed = is_subscribed
        super(Subscription, self).__init__(db="subscription_db")

    def subscribe(self) -> str:
        self.db.put({'key': self.key, 'is_subscribed': self.is_subscribed})
        logging.info(f"{self.key} is successfully subscribed.")
        return f"{self.key} is successfully subscribed."

    def unsubscribe(self) -> str:
        self.db.update({'is_subscribed': False}, self.key)
        logging.info(f"{self.key} is successfully unsubscribed.")
        return f"{self.key} is successfully unsubscribed."

    def _validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
