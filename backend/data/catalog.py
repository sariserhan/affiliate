import logging

from .database import DETA

logging.basicConfig(level=logging.DEBUG)

class Catalog(DETA):
    
    def __init__(self, name: str = ''):
        self.name = name
        self.key = name.replace(' ','_')
        super(Catalog, self).__init__(db="catalog_db")
        
    def create_catalog(self, name: str):
        self.key = name.replace(' ','_')
        self.name = name
        
        data = {
            "key": self.key,
            "name": self.name,
            "is_active": False,
            "item_list": []
        }
        try:
            self.db.insert(data)
            logging.info(f"{self.name} is successfully added.")
            return f"{self.name} is successfully added."
        except:
            logging.warning(f"{self.name} is already in the database.")
        return
        
    
    def add_item(self, items:list):
        if not self.name == '':
            catalog = self.db.get(self.key)
            if not catalog:
                self.create_catalog(name=self.name)
                catalog = self.db.get(self.key)
            catalog['item_list'].extend(items)
            self.db.put(catalog)
            logging.info(f"{items} are added to {self.name} catalog.")
            return f"{items} are added to {self.name} catalog."
        else:
            logging.warning("catalog name required.")
            return
    
        
if __name__ == '__main__':
    pass
    # new_catalog = Catalog(name='catalog test3')
    # new_catalog.create_catalog()
    # new_catalog.change_catalog({'name': 'TV 88', 'is_active': True, 'asas':1})
    # new_catalog.add_item(items=['new_item4', 'asd'])
    # print(new_catalog.fetch_items())
    # new_catalog.delete_item(new_catalog.key)
    