import logging

from .database import DETA

logging.basicConfig(level=logging.DEBUG)


class Affiliate_Partner(DETA):
    
    def __init__(self):
        super(Affiliate_Partner, self).__init__(db="affiliate_partner_db")
    
    def create_partner(self, name: str, email_account=None, password=None):
        data = {
            "key": name,
            "email_account": email_account,
            "password": password,
        }
        try:
            self.db.insert(data)
            logging.info(f"{name} is successfully added.")
            return f"{name} is successfully added."
        except:
            logging.warning(f"{name} is already in the database.")
        return
    
if __name__ == '__main__':
    pass