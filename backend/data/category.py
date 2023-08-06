import logging

from .database import DETA

logging.basicConfig(level=logging.DEBUG)


class Category(DETA):

    def __init__(self, name: str = ''):
        self.name = name
        self.key = name.replace(' ', '_')
        super(Category, self).__init__(db="category_db")

    def create_category(self, name: str):
        self.key = name.replace(' ', '_')
        self.name = name

        data = {
            "key": self.key,
            "name": self.name,
            "is_active": True,
            "catalog_list": []
        }
        try:
            self.db.insert(data)
            logging.info(f"{self.name} is successfully added.")
            return f"{self.name} is successfully added."
        except Exception:
            logging.warning(f"{self.name} is already in the database.")
        return

    def add_catalog(self, catalogs: list):
        if self.name != '':
            category = self.db.get(self.key)
            if not category:
                self.create_category(name=self.name)
                category = self.db.get(self.key)
            category['catalog_list'].extend(catalogs)  # type: ignore
            self.db.put(category)  # type: ignore
            logging.info(f"{catalogs} is added to {self.name} category.")
            return f"{catalogs} is added to {self.name} category."
        else:
            logging.warning("category name required.")
            return


if __name__ == '__main__':
    # categories = Category().migrate_database('category_db_backup')
    categories = Category().fetch_records()
    for category in categories:
        Category().update_record(
            key=category['key'], updates={'catalog_list': []})
