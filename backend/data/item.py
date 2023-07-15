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

    def create_item(self, name: str, description: str, image_path: str, image_name: str, affiliate_link: str, catalog_names: list, f_clicked: int = 0):        
        for catalog_name in catalog_names:
            key = name.replace(' ',f'_{catalog_name}')
            data = {
                "key": key,
                "name": name,
                "description": description,
                "affiliate_link": affiliate_link,
                "image_name": image_name,
                "clicked": 0,
                "f_clicked": f_clicked,
                "catalog": catalog_name,
                "sent": False
            }

            try:
                # Load data in to items_db Base
                self.db.insert(data)
            except:
                logging.warning(f"{name} is already in the database.")        
         
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
    