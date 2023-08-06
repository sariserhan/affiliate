import json
import logging

from .affiliate_partner import Affiliate_Partner
from .catalog import Catalog
from .category import Category
from .database import DETA

logging.basicConfig(level=logging.DEBUG)


class Item(DETA):

    def __init__(self, name: str = ''):
        super(Item, self).__init__(db="items_db2")

    def create_item(self,
                    name: str,
                    description: str,
                    image_path: str,
                    pros: str, cons: str,
                    image_name: str,
                    affiliate_link: str,
                    affiliate_partner: str,
                    categories: list,
                    catalog_names: list,
                    f_clicked: int = 0
                    ):
        for catalog_name in catalog_names:
            name = name.strip()
            key = name.replace(' ', '_')
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
                "categories": categories,
                "pros": pros,
                "cons": cons,
                "email_sent": False
            }

            try:
                # Load data in to items_db Base
                self.db.insert(data)
            except Exception:
                logging.warning(f"{name} is already in the database.")

            # Upload image in to image_db Drive
            self.drive.put(f'{catalog_name}/{image_name}', image_path)

            # Add item into catalog
            catalog_obj = Catalog(catalog_name)
            catalog_obj.add_item(items=[name])

            # Create Affiliate Partner
            affiliate_partner_obj = Affiliate_Partner()
            affiliate_partner_obj.create_partner(name=affiliate_partner)

        for category in categories:
            # Add catalog into category
            category_obj = Category(category)
            category_obj.add_catalog(catalogs=catalog_names)

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


# if __name__ == '__main__':
    # Item().migrate_database('items_db_backup')
    # items = Item().fetch_records()
    # for item in items:
    #     new_category = []
    #     for category in item['categories']:
    #         if 'Equipment' in category and not 'Equipments' in category:
    #             category = category+'s'
    #         new_category.append(category)

    #     Item().update_record(item['key'], updates={'categories': new_category})

    # catalog_list = []
    # for item in items:
    #     catalog = item['catalog']
    #     if catalog not in catalog_list:
    #         catalog_list.append(catalog)
    #         name = item['name']
    #         key = item['key']
    #         item_categories = item['categories']
    #         for item_category in item_categories:
    #             category = Category(item_category)
    #             category.add_catalog(catalogs=[catalog])

    # if len(item['categories']) == 0:
    #     logging.info(catalog)

    # if catalog == 'TV Antenna':
    #     category_list = [
    #         "Electronics",
    #         "Computer_Hardware",
    #         "Computer_Accessories"
    #     ]
    # elif catalog == 'External Hard Drive':
    #     category_list = [
    #         "Computer_Hardware",
    #         "Computer_Accessories"
    #     ]
    # elif catalog == 'Surge Protector':
    #     category_list = [
    #         "Electronics"
    #     ]
    # elif catalog == 'Cable Modem':
    #     category_list = [
    #         "Networking Equipment"
    #     ]
    # elif catalog == 'Gaming Mouse':
    #     category_list = [
    #         "Gaming",
    #         "Computer_Accessories"
    #     ]
    # elif catalog == 'Wi-Fi 6 Router':
    #     category_list = [
    #         "Networking Equipment"
    #     ]
    # elif catalog == 'Gaming Laptop':
    #     category_list = [
    #         "Gaming",
    #         "Laptop_Computers"
    #     ]
    # elif catalog == 'Adjustable Dumbbells':
    #     category_list = [
    #         "Fitness Equipment"
    #     ]
    # elif catalog == 'Chromebook':
    #     category_list = [
    #         "Laptop Computers"
    #     ]
    # elif catalog == 'Smart Thermostat':
    #     category_list = [
    #         "Home Devices"
    #     ]
    # elif catalog == 'Monitor':
    #     category_list = [
    #         "Computer Accessories",
    #         "Computer Hardware"
    #     ]
    # elif catalog == 'Portable Charger':
    #     category_list = [
    #         "Electronics",
    #         "Mobile Accessories"
    #     ]
    # elif catalog == 'Webcam':
    #     category_list = [
    #         "Computer Accessories",
    #         "Computer Hardware"
    #     ]
    # elif catalog == 'Outdoor Camera':
    #     category_list = [
    #         "Home Devices",
    #         "Home Security"
    #     ]
    # elif catalog == 'Smart Lock':
    #     category_list = [
    #         "Home Devices",
    #         "Home Security"
    #     ]
    # elif catalog == 'Gaming|Streaming Microphone':
    #     category_list = [
    #         "Computer Accessories",
    #         "Computer Hardware",
    #         "Gaming"
    #     ]
    # elif catalog == 'Treadmill':
    #     category_list = [
    #         "Fitness Equipment"
    #     ]
    # elif catalog == 'Soundbar':
    #     category_list = [
    #         "Audio Equipment",
    #         "Home Entertainment"
    #     ]
    # elif catalog == 'Coffee Maker':
    #     category_list = [
    #         "Kitchen Appliances"
    #     ]
    # elif catalog == 'Mattress (King)':
    #     category_list = [
    #         "Furniture"
    #     ]
    # elif catalog == 'Printer':
    #     category_list = [
    #         "Electronics",
    #         "Office Equipment"
    #     ]
    # elif catalog in ['Running Belt', 'Exercise Bike', 'Treadmill', 'Water Bottle']:
    #     category_list = [
    #         "Fitness Equipment"
    #     ]
    # elif catalog == 'Bread Maker':
    #     category_list = [
    #         "Kitchen Appliances"
    #     ]
    # elif catalog == 'Stand Mixer':
    #     category_list = [
    #         "Kitchen Appliances"
    #     ]
    # elif catalog == 'Garlic Press':
    #     category_list = [
    #         "Kitchen Appliances"
    #     ]
    # elif catalog == 'Photo Printer':
    #     category_list = [
    #         "Office Equipment",
    #         "Electronics"
    #     ]
    # elif catalog == 'Gaming Keyboard':
    #     category_list = [
    #         "Gaming",
    #         "Computer Accessories",
    #         "Computer Hardware"
    #     ]
    # elif catalog == 'Gaming Mouse Pad':
    #     category_list = [
    #         "Gaming",
    #         "Computer Accessories",
    #         "Computer Hardware"
    #     ]
    # elif catalog == 'Solar Light':
    #     category_list = [
    #         "Electronics"
    #     ]
    # elif catalog == 'Mini Computer':
    #     category_list = [
    #         "Laptop Computers"
    #     ]
    # elif catalog == 'Wi-Fi Extender':
    #     category_list = [
    #         "Networking Equipment"
    #     ]
    # elif catalog == 'Action Camera':
    #     category_list = [
    #         "Camera"
    #     ]
    # elif catalog == 'Streaming Device':
    #     category_list = [
    #         "Entertainment Devices",
    #         "Home Entertainment"
    #     ]
    # elif catalog == 'Standing Desk':
    #     category_list = [
    #         "Office Equipments"
    #     ]
    # elif catalog == 'Electric Bike':
    #     category_list = [
    #         "Entertainment Devices",
    #         "Electronics"
    #     ]
    # elif catalog == 'Under-Desk Treadmill':
    #     category_list = [
    #         "Office Equipments",
    #         "Fitness Equipment"
    #     ]
    # elif catalog == 'Cross Training Shoes':
    #     category_list = [
    #         "Fitness Equipment"
    #     ]
    # elif catalog == 'Dash Cam':
    #     category_list = [
    #         "Automotive Accessories",
    #         "Camera"
    #     ]
    # elif catalog == 'Portable Printer':
    #     category_list = [
    #         "Office Equipments",
    #         "Electronics"
    #     ]
    # elif catalog == 'Electric Scooter':
    #     category_list = [
    #         "Entertainment Devices",
    #         "Electronics"
    #     ]
    # elif catalog == 'VR Headset':
    #     category_list = [
    #         "Gaming",
    #         "Computer Accessories",
    #         "Computer Hardware"
    #     ]
    # elif catalog == 'Massage Gun':
    #     category_list = [
    #         "Massage Devices"
    #     ]
    # elif catalog == 'Action Camera':
    #     category_list = [
    #         "Camera"
    #     ]
    # elif catalog == 'iPhone Lenses':
    #     category_list = [
    #         "Mobile Accessories"
    #     ]
    # elif catalog == '8K TV':
    #     category_list = [
    #         "Home Entertainment"
    #     ]
    # elif catalog == 'OLED TV':
    #     category_list = [
    #         "Home Entertainment"
    #     ]
    # elif catalog == 'Outdoor Speaker':
    #     category_list = [
    #         "Audio Equipment"
    #     ]

    # if category_list:
    #     Item().update_record(key, {'categories': category_list})
    #     logging.info(f'Category List updateed for: {name}')
