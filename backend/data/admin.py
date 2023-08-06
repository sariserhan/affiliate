import logging
import re

from .database import DETA

logging.basicConfig(level=logging.DEBUG)


class Admin(DETA):

    def __init__(self):
        super(Admin, self).__init__(db="admin_db")

    def create_user(self, name: str, username: str, password: str):
        if not self._validate_username(username):
            raise ValueError("Invalid email address")
        self.name = name
        self.key = username
        self.password = password

    def _validate_username(self, username):
        # Check for spaces
        if ' ' in username:
            return False

        # Check for special characters
        return bool(re.match("^[a-zA-Z0-9_]+$", username))
