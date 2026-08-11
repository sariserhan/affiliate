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
            logging.info("%s is successfully added.", self.name)
            return f"{self.name} is successfully added."
        except Exception:
            logging.warning("%s is already in the database.", self.name)
        return

    def add_catalog(self, catalogs: list):
        if self.name != '':
            category = self.get_record(key=self.key)
            if not category:
                self.create_category(name=self.name)
                category = self.get_record(key=self.key)

            new_catalogs = [c for c in catalogs if c not in category['catalog_list']]
            if new_catalogs:
                category['catalog_list'].extend(new_catalogs)  # type: ignore
                self.db.put(category)  # type: ignore
                logging.info("%s is added to %s category.",
                             new_catalogs, self.name)
                return f"{new_catalogs} is added to {self.name} category."
        else:
            logging.warning("catalog name required.")
            return


if __name__ == '__main__':
    # categories = Category().migrate_database('category_db_backup')
    # categories = Category().fetch_records()
    # for category in categories:
    #     Category().update_record(
    #         key=category['key'], updates={'catalog_list': []})

    print(Category().get_record(key='Audio_Equipments')['catalog_list'])
