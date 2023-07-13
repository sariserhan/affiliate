import logging
import os

from deta import Deta
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

class DETA:
    
    def __init__(self, db: str) -> None:
        self.deta = Deta(os.getenv("DETA_KEY"))
        self.db = self.deta.Base(db)
        self.drive = self.deta.Drive('images_db')
        
    def fetch_records(self) -> list:
        return self.db.fetch().items
    
    def get_record(self, key: str) -> str:        
        return self.db.get(key)
    
    def get_image_data(self, name: str, catalog: str) -> str:        
        return self.drive.get(f"/{catalog}/{name}").read()
    
    def get_record_by_catalog(self, catalog: str) -> list:
        records = self.fetch_records()
        records_list = []
        for record in records:
            if catalog == record['catalog']:
                records_list.append(record)
        return records_list
    
    def change_record(self, key: str, updates: dict) -> str:
        record = self.db.get(key)
        for k, v in updates.items():
            if k in record:
                record[k] = v

        self.delete_item(key)
        if 'name' in record:
            record['key'] = record['name'].replace(' ','_')
                
        self.db.put(record)
        
        logging.info(f"{key} successfully changed record.")
        return f"{key} successfully changed record."
    
    def delete_item(self, key: str) -> str:
        self.db.delete(key)
        logging.info(f"{key} successfully deleted.")
        return f"{key} successfully deleted."


if __name__ == '__main__':
    pass
    # deta = DETA('images_db')
    # image = deta.get_image_data(name='Helix Midnight Luxe (Queen)', catalog='Mattress')