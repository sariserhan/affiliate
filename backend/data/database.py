import logging
import os
from dataclasses import dataclass
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.types.json import Jsonb

logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()


def ensure_schema(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS kv_store (
                collection text NOT NULL,
                key text NOT NULL,
                data jsonb NOT NULL,
                updated_at timestamptz DEFAULT now(),
                PRIMARY KEY (collection, key)
            )
            """
        )


def get_connection() -> psycopg.Connection:
    conn = psycopg.connect(os.getenv("DATABASE_URL"), autocommit=True)
    ensure_schema(conn)
    return conn


@dataclass
class FetchResult:
    items: list


class KVTable:
    def __init__(self, collection: str, conn: psycopg.Connection):
        self.collection = collection
        self.conn = conn

    def insert(self, data: dict) -> dict:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO kv_store (collection, key, data) VALUES (%s, %s, %s)",
                (self.collection, data["key"], Jsonb(data)),
            )
        return data

    def put(self, data: dict) -> dict:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO kv_store (collection, key, data, updated_at)
                VALUES (%s, %s, %s, now())
                ON CONFLICT (collection, key)
                DO UPDATE SET data = EXCLUDED.data, updated_at = now()
                """,
                (self.collection, data["key"], Jsonb(data)),
            )
        return data

    def get(self, key: str):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT data FROM kv_store WHERE collection = %s AND key = %s",
                (self.collection, key),
            )
            row = cur.fetchone()
        return row[0] if row else None

    def update(self, updates: dict, key: str):
        record = self.get(key)
        if record is None:
            return None
        record.update(updates)
        return self.put(record)

    def delete(self, key: str) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM kv_store WHERE collection = %s AND key = %s",
                (self.collection, key),
            )

    def fetch(self) -> FetchResult:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT data FROM kv_store WHERE collection = %s",
                (self.collection,),
            )
            rows = cur.fetchall()
        return FetchResult(items=[row[0] for row in rows])


class LocalDrive:
    def __init__(self, root: str):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, path: str) -> Path:
        return self.root / path.lstrip("/")

    def put(self, path: str, data: bytes) -> str:
        file_path = self._resolve(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(data)
        return path

    def get(self, path: str):
        file_path = self._resolve(path)
        if not file_path.exists():
            return None
        return _DriveFile(file_path)

    def delete(self, path: str) -> None:
        file_path = self._resolve(path)
        if file_path.exists():
            file_path.unlink()

    def list(self) -> dict:
        names = [
            str(p.relative_to(self.root))
            for p in self.root.rglob("*")
            if p.is_file()
        ]
        return {"names": names}


class _DriveFile:
    def __init__(self, path: Path):
        self._path = path

    def read(self) -> bytes:
        return self._path.read_bytes()


def get_drive() -> LocalDrive:
    return LocalDrive(root=os.getenv("IMAGE_STORAGE_PATH", "./local_images"))


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
