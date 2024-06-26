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
        self.deta = Deta(os.getenv("DETA_KEY"))  # type: ignore
        self.db = self.deta.Base(db)
        self.drive = self.deta.Drive('images_db')

    def fetch_records(self) -> list:
        return self.db.fetch().items

    def get_record(self, key: str) -> str:
        return self.db.get(key)  # type: ignore

    def get_image_data(self, name: str, catalog: str) -> str:
        return self.drive.get(f"/{catalog}/{name}").read()  # type: ignore

    def del_image_data(self, name: str, catalog: str) -> str:
        return self.drive.delete(f"/{catalog}/{name}")

    def get_image_names(self):
        return self.drive.list()['names']

    def get_record_by_catalog(self, catalog: str) -> list:
        records = self.fetch_records()
        return [record for record in records if catalog == record['catalog']]

    def update_record(self, key: str, updates: dict) -> str:  # type: ignore
        record = self.db.get(key)
        for k, v in updates.items():
            if k in record:
                record[k] = v  # type: ignore
        try:
            logging.info(f'Updated: {key}')
            return self.db.put(record)  # type: ignore
        except Exception as e:
            logging.error(f'Error in Updating: {key} ---> {e}')

    def add_new_attribute(self, key: str, new_attr: dict):
        attributes = self.db.get(key=key)
        attributes.update(new_attr)
        self.db.put(key=key, data=new_attr)

    def change_record(self, key: str, updates: dict) -> str:
        record = self.db.get(key)
        for k, v in updates.items():
            if k in record:
                record[k] = v  # type: ignore

        self.delete_item(key)
        if 'name' in record:  # type: ignore
            record['key'] = record['name'].replace(' ', '_')  # type: ignore

        self.db.put(record)  # type: ignore

        logging.info(f"{key} successfully changed record.")
        return f"{key} successfully changed record."

    def delete_item(self, key: str):
        name = key
        key = key.replace(' ', '_')
        try:
            catalog_name = self.get_record(key)['catalog']  # type: ignore
            catalog_base = self.deta.Base("catalog_db")
            catalog_record = catalog_base.get(key=catalog_name)
            for item in catalog_record['item_list']:  # type: ignore
                if item == name:
                    catalog_record['item_list'].remove(item)  # type: ignore
                    break
            catalog_base.put(catalog_record)  # type: ignore
            logging.info("%s successfully removed from catalog.", name)
        except Exception as e:
            logging.error('Error in removing %s from catalog ---> %s', name, e)
        try:
            self.db.delete(key)
            logging.info("%s successfully deleted.", name)
            return True
        except Exception as e:
            logging.error('Error in deleting %s ---> %s', name, e)
            return False

    def migrate_database(self, target_database: str):
        target = self.deta.Base(target_database)

        for item in self.db.fetch().items:
            if not item['key'].startswith('Corsair'):
                try:
                    target.put(item)
                    logging.info('%s is migrated!', item["key"])
                except Exception as e:
                    logging.error('Error migrating %s --> %s', item["key"], e)
                    raise e
        return


if __name__ == '__main__':
    # DETA('item_db').migrate_database(target_database='items_db2')
    DETA('item_db2').del_image_data(
        name='Nathan Running Handheld Quick Squeeze.jpeg', catalog='Water Bottle')
