import json
import logging

from .catalog import Catalog
from .affiliate_partner import Affiliate_Partner
from .database import DETA

logging.basicConfig(level=logging.DEBUG)

class Item(DETA):
    
    def __init__(self, name: str = ''):
        super(Item, self).__init__(db="items_db2")

    def create_item(self, name: str, description: str, image_path: str, pros: str, cons: str, image_name: str, affiliate_link: str, affiliate_partner: str, catalog_names: list, f_clicked: int = 0):        
        for catalog_name in catalog_names:
            name = name.strip()
            key = name.replace(' ',f'_')
            data = {
                "key": key,
                "name": name,
                "description": description,
                "affiliate_link": affiliate_link,
                "affiliate_partner": affiliate_partner,
                "image_name": image_name,
                "clicked": 0,
                "f_clicked": f_clicked,
                "catalog": catalog_name,
                "pros": pros,
                "cons": cons,
                "email_sent": False
            }

            try:
                # Load data in to items_db Base
                self.db.insert(data)
            except:
                logging.warning(f"{name} is already in the database.")        
         
            # Upload image in to image_db Drive
            self.drive.put(f'{catalog_name}/{image_name}', image_path)

            # Add item into catalog
            catalog_obj = Catalog(catalog_name)
            catalog_obj.add_item(items=[name])     
            
            # Create Affiliate Partner
            affiliate_partner_obj = Affiliate_Partner()
            affiliate_partner_obj.create_partner(name=affiliate_partner)
        
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
    