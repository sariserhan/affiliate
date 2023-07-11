import base64
import logging
import json

from matplotlib import category

from .catalog import Catalog
from .database import DETA
from typing import Union

logging.basicConfig(level=logging.DEBUG)

class Item(DETA):
    
    def __init__(self, name: str = ''):
        super(Item, self).__init__(db="items_db")

    def create_item(self, name: str, description: str, image_path: str, image_name: str, affiliate_link: str, catalog_name: str, clicked: int = 0, f_clicked: int = 0):        
        key = name.replace(' ','_')  
        data = {
            "key": key,
            "name": name,
            "description": description,
            "affiliate_link": affiliate_link,
            "image_name": image_name,
            "clicked": clicked,
            "f_clicked": f_clicked,
            "catalog": catalog_name
        }

        try:
            # Load data in to items_db Base
            self.db.insert(data)
        except Exception as e:
            logging.warning(f"{name} is already in the database.")
            raise e
        
        # Upload image in to image_db Drive
        self.drive.put(f'{catalog_name}/{image_name}', image_path)
    
        # Add item into catalog
        catalog = Catalog(catalog_name)
        catalog.add_item(items=[name])     
        
        logging.info(f"{name} is successfully added to the database.")
        return f"{name} is successfully added to the database."
    
    @staticmethod
    def _process_data(data):
        if isinstance(data, bytes):
            # Convert bytes to string, ignoring decoding errors
            data = data.decode('utf-8', errors='ignore')
        # Process the data or perform any necessary transformations
        processed_data = data.upper()
        return json.dumps(processed_data)


if __name__ == '__main__':
    pass
    # item = Item()
    # item.create_item(name='sonytv447', description='testttttt4', image_path='assets/findik.png', image_name='findik.png' ,affiliate_link='wasdsd', catalog_name='new-test-catalog')
    
    # item.change_record(key='sony_tv88', updates={'description': 'sari'})
    # print(item.get_record_by_catalog(catalog='TV_7'))
    # print(item.fetch_records())
    # print(item.get_record(key='sony_tv'))
    
    