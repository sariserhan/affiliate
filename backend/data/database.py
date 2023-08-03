import logging
import os
import ssl

from deta import Deta
from dotenv import load_dotenv
from streamlit import secrets

ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

class DETA:
    
    def __init__(self, db: str) -> None:
        self.deta = Deta(os.getenv("DETA_KEY") or secrets("DETA_KEY"))
        self.db = self.deta.Base(db)
        self.drive = self.deta.Drive('images_db')
        
    def fetch_records(self) -> list:
        return self.db.fetch().items
    
    def get_record(self, key: str) -> str:        
        return self.db.get(key)
    
    def get_image_data(self, name: str, catalog: str) -> str:        
        return self.drive.get(f"/{catalog}/{name}").read()
    
    def del_image_data(self, name: str, catalog: str) -> str:        
        return self.drive.delete(f"/{catalog}/{name}")
    
    def get_record_by_catalog(self, catalog: str) -> list:
        records = self.fetch_records()
        return [record for record in records if catalog == record['catalog']]
    
    def update_record(self, key:str, updates: dict) -> str:
        record = self.db.get(key)
        for k, v in updates.items():
            if k in record:
                record[k] = v
                
        self.db.put(record)
    
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
    
    def delete_item(self, key: str):
        name = key
        key = key.replace(' ','_')
        try:
            catalog_name = self.get_record(key)['catalog']
            catalog_base = self.deta.Base("catalog_db")
            catalog_record = catalog_base.get(key=catalog_name)
            for item in catalog_record['item_list']:
                if item == name:
                    catalog_record['item_list'].remove(item)
                    break
            catalog_base.put(catalog_record)
            logging.info(f"{name} successfully removed from catalog.")
        except Exception as e:
            logging.error(f'Error in removing {name} from catalog ---> {e}')
        try:
            self.db.delete(key)
            logging.info(f"{name} successfully deleted.")
            return True
        except Exception as e:
            logging.error(f'Error in deleting {name} ---> {e}')
            return False
        
    def migrate_database(self, target_database: str):        
        target = self.deta.Base(target_database)        

        for item in self.db.fetch().items:
            if not item['key'].startswith('Corsair'):
                try:
                    target.insert(item)
                    logging.info(f'{item["key"]} is migrated!')
                except Exception as e:
                    logging.error(f'Error migrating {item["key"]} --> {e}')
                    raise e
        return
                

if __name__ == '__main__':
    # DETA('item_db').migrate_database(target_database='items_db2')
    DETA('item_db2').del_image_data(name='Nathan Running Handheld Quick Squeeze.jpeg', catalog='Water Bottle')
    
