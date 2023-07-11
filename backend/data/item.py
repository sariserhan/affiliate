import base64
import logging
import json

from .catalog import Catalog
from .database import DETA
from typing import Union

logging.basicConfig(level=logging.DEBUG)

class Item(DETA):
    
    def __init__(self, name: str = ''):
        super(Item, self).__init__(db="items_db")

    def create_item(self, name: str, description: str, image_path_or_byte: Union[str, bytes], affiliate_link: str, catalog_name: str, clicked: int = 0):
        self.name = name
        self.key = name.replace(' ','_')    
        if type(image_path_or_byte) is str:
            with open(image_path_or_byte, 'rb') as file:
                image_data = file.read() 
            base64_data = base64.b64encode(image_data).decode('utf-8')
        else:
            print("SERHAN--------------------")
            base64_data = self._process_data(image_path_or_byte)
            
        data = {
            "key": self.key,
            "name": self.name,
            "description": description,
            "image_data": base64_data,
            "affiliate_link": affiliate_link,
            "clicked": clicked,
            "catalog": catalog_name
        }
        print(data['description'])
        print("SERHAN")
        self.db.put(data)
        print("SARI")
        catalog = Catalog(catalog_name)
        catalog.add_item(items=[self.name])
                
        
        
        logging.info(f"{self.name} is successfully added to the database.")
        return f"{self.name} is successfully added to the database."
        # except:
        #     logging.warning(f"{self.name} is already in the database.")
        #     return
    
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
    # item.create_item(name='sonytv4', description='test4', image_path_or_byte='assets/linkedin-icon.png', link='wasdsd', catalog_name='tv')
    # item.change_record(key='sony_tv88', updates={'description': 'sari'})
    # print(item.get_record_by_catalog(catalog='TV_7'))
    # print(item.fetch_records())
    # print(item.get_record(key='sony_tv'))
    
    