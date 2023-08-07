import logging

from .database import DETA

logging.basicConfig(level=logging.DEBUG)


class Catalog(DETA):

    def __init__(self, name: str = ''):
        self.name = name
        self.key = name.replace(' ', '_')
        super(Catalog, self).__init__(db="catalog_db")

    def create_catalog(self, name: str):
        self.key = name.replace(' ', '_')
        self.name = name

        data = {
            "key": self.key,
            "name": self.name,
            "is_active": True,
            "item_list": []
        }
        try:
            self.db.insert(data)
            logging.info("%s is successfully added.", self.name)
            return f"{self.name} is successfully added."
        except Exception:
            logging.warning("%s is already in the database.", self.name)
        return

    def add_item(self, items: list):
        if self.name != '':
            catalog = self.db.get(self.key)
            if not catalog:
                self.create_catalog(name=self.name)
                catalog = self.db.get(self.key)
            catalog['item_list'].extend(items)  # type: ignore
            self.db.put(catalog)  # type: ignore
            logging.info("%s are added to %s catalog.", items, self.name)
            return f"{items} are added to {self.name} catalog."
        else:
            logging.warning("catalog name required.")
            return


if __name__ == '__main__':
    # catalogs = Catalog().fetch_records()
    Catalog().migrate_database('catalog_db_backup')
