import base64
import logging

from .catalog import Catalog
from .database import DETA
from typing import Union

logging.basicConfig(level=logging.DEBUG)

class Item(DETA):
    
    def __init__(self, name: str = ''):
        self.name = name
        self.key = name.replace(' ','_')       
        super(Item, self).__init__(db="items_db")        

    def create_item(self, name: str, description: str, image_path_or_byte: Union[str, bytes], link: str, catalog_name: str, clicked: int = 0):
        if type(image_path_or_byte) is str:
            with open(image_path_or_byte, 'rb') as file:
                image_data = file.read() 
            base64_data = base64.b64encode(image_data).decode('utf-8')
        else:
            base64_data = image_path_or_byte
            
        data = {
            "key": self.key,
            "name": self.name,
            "description": description,
            "image_data": base64_data,
            "link": link,
            "clicked": clicked,
            "catalog": catalog_name
        }
        catalog = Catalog(catalog_name)
        catalog.add_item(items=[self.name])
                
        try:
            self.db.insert(data)
            logging.info(f"{self.name} is successfully added to the database.")
            return f"{self.name} is successfully added to the database."
        except:
            logging.warning(f"{self.name} is already in the database.")
            return


if __name__ == '__main__':
    item = Item()
    item.create_item(name='sonytv4', description='test4', image_path_or_byte='assets/linkedin-icon.png', link='wasdsd', catalog_name='tv')
    # item.change_record(key='sony_tv88', updates={'description': 'sari'})
    # print(item.get_record_by_catalog(catalog='TV_7'))
    # print(item.fetch_records())
    # print(item.get_record(key='sony_tv'))
    
    