# Deta -> Railway Postgres/Volume Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the retired Deta Base/Drive backend with a Postgres-backed key-value shim (Railway Postgres) and a local-disk-backed drive shim (Railway Volume), without changing any call sites in `backend/data/catalog.py`, `item.py`, `category.py`, `subscribe.py`, `affiliate_partner.py`, or `admin.py`.

**Architecture:** A generic `kv_store(collection, key, data jsonb)` Postgres table backs a `KVTable` class implementing Deta Base's `insert/put/get/update/delete/fetch` interface. A `LocalDrive` class backed by a directory (Railway Volume mount) implements Deta Drive's `put/get/delete/list` interface. The existing `DETA` base class in `backend/data/database.py` is rewired to construct these instead of a real Deta client; every subclass keeps working unchanged.

**Tech Stack:** psycopg 3 (raw SQL, no ORM), Postgres (Railway), local filesystem (Railway Volume), pytest (already in the repo).

## Global Constraints

- No changes to the six `backend/data/{catalog,item,category,subscribe,affiliate_partner,admin}.py` files — only `backend/data/database.py` and `backend/email/send_email.py` change.
- Single generic `kv_store` table — no per-collection tables, no relational redesign (see spec's "Non-goals").
- `requirements.txt`: remove `deta==1.2.0`, add `psycopg[binary]>=3.1` (unpinned floor, not an exact pin — the incident that started this migration was an exact pin to a version that never existed).
- Env vars: `DETA_KEY` is replaced by `DATABASE_URL`; new `IMAGE_STORAGE_PATH` var (default `./local_images` for local dev).
- Images are stored as files under `IMAGE_STORAGE_PATH`; the app never needs public URLs for them (confirmed: every image read goes through `get_image_data(...).read()` → `PIL.Image.open(BytesIO(...))`).
- Test additions use plain pytest `assert` statements only — no fixtures, no mocking libraries. Tests that need a live Postgres are skipped (not failed) when `DATABASE_URL` isn't set, so the existing CI `pytest` step (which has no `DATABASE_URL`) keeps passing.

---

### Task 1: Postgres connection, schema, and dependency setup

**Files:**
- Modify: `requirements.txt`
- Create: `.env.example`
- Modify: `backend/data/database.py` (new top-of-file content only — `get_connection`, `ensure_schema`, `get_drive`; the `DETA` class itself is rewired in Task 4)

**Interfaces:**
- Produces: `get_connection() -> psycopg.Connection` (autocommit, schema already ensured), `ensure_schema(conn: psycopg.Connection) -> None`, `get_drive() -> LocalDrive` (from Task 3)

- [ ] **Step 1: Swap the dependency in `requirements.txt`**

Replace:
```
deta==1.2.0
```
with:
```
psycopg[binary]>=3.1
```

- [ ] **Step 2: Install it**

Run: `pip install -r requirements.txt`
Expected: `psycopg` installs successfully (no "no matching distribution" error).

- [ ] **Step 3: Document the new env vars**

Create `.env.example` at the repo root:
```
# Postgres connection string, e.g. from Railway's Postgres plugin
DATABASE_URL=postgresql://user:password@host:5432/railway

# Directory where item images are stored (mount a Railway Volume here in production)
IMAGE_STORAGE_PATH=./local_images

# --- Existing app config (unrelated to this migration, unchanged) ---
# OPENAI_API_KEY=
# GOOGLE_ANALYTICS_TAG_ID=
# GOOGLE_ADSENSE_ID=
# IMPACT_ID=
# STREAMLIT_ANALYTICS=
# email_sender_name=
# email_password=
```

- [ ] **Step 4: Replace the top of `backend/data/database.py`**

Replace the current imports and `ssl`/`DETA` setup at the top of the file (lines 1–15, everything before `class DETA:`) with:

```python
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
```

Leave the rest of the file (the `class DETA:` block and everything below) untouched for now — it's rewritten in Task 4. The file will not fully work yet; that's expected until Task 4 lands.

- [ ] **Step 5: Verify it connects against a real Postgres**

You need a reachable Postgres for this and every later task's tests. The fastest option for local development:

Run: `docker run --rm -d --name deta-migration-pg -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16`

Then set: `export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres`

Run:
```bash
python3 -c "
from backend.data.database import get_connection
conn = get_connection()
print('connected:', conn.info.status)
"
```
Expected: prints `connected: ConnStatus.OK` and does not raise. This also confirms `ensure_schema` created the `kv_store` table — verify with:
```bash
python3 -c "
from backend.data.database import get_connection
conn = get_connection()
with conn.cursor() as cur:
    cur.execute(\"SELECT to_regclass('kv_store')\")
    print(cur.fetchone())
"
```
Expected: `('kv_store',)`, not `(None,)`.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt .env.example backend/data/database.py
git commit -m "chore: swap deta dependency for psycopg, add Postgres connection helper"
```

---

### Task 2: `KVTable` — Postgres-backed replacement for Deta Base

**Files:**
- Modify: `backend/data/database.py` (add `FetchResult` dataclass and `KVTable` class, above `class DETA:`)
- Test: `backend/data/test_database.py` (new)

**Interfaces:**
- Consumes: `get_connection() -> psycopg.Connection` (Task 1)
- Produces: `KVTable(collection: str, conn: psycopg.Connection)` with methods `insert(data: dict) -> dict`, `put(data: dict) -> dict`, `get(key: str) -> dict | None`, `update(updates: dict, key: str) -> dict | None`, `delete(key: str) -> None`, `fetch() -> FetchResult` where `FetchResult.items: list[dict]`. All methods take `data["key"]` / the `key` argument as the record's primary key within its collection.

- [ ] **Step 1: Write the failing tests**

Create `backend/data/test_database.py`:

```python
import os
import uuid

import pytest

from backend.data.database import KVTable, get_connection

requires_postgres = pytest.mark.skipif(
    not os.getenv("DATABASE_URL"),
    reason="requires a live Postgres reachable via DATABASE_URL",
)


def _table() -> KVTable:
    # unique collection per test run so tests never collide with real data
    return KVTable(collection=f"test_{uuid.uuid4().hex}", conn=get_connection())


@requires_postgres
def test_insert_then_get_returns_the_record():
    table = _table()
    table.insert({"key": "widget", "name": "Widget"})
    assert table.get("widget") == {"key": "widget", "name": "Widget"}


@requires_postgres
def test_get_missing_key_returns_none():
    table = _table()
    assert table.get("does-not-exist") is None


@requires_postgres
def test_insert_duplicate_key_raises():
    table = _table()
    table.insert({"key": "widget", "name": "Widget"})
    with pytest.raises(Exception):
        table.insert({"key": "widget", "name": "Widget Again"})


@requires_postgres
def test_insert_duplicate_key_does_not_break_the_connection():
    table = _table()
    table.insert({"key": "widget", "name": "Widget"})
    try:
        table.insert({"key": "widget", "name": "Widget Again"})
    except Exception:
        pass
    # the connection must still be usable after a caught insert failure
    table.put({"key": "other", "name": "Other"})
    assert table.get("other") == {"key": "other", "name": "Other"}


@requires_postgres
def test_put_creates_when_missing():
    table = _table()
    table.put({"key": "widget", "name": "Widget"})
    assert table.get("widget") == {"key": "widget", "name": "Widget"}


@requires_postgres
def test_put_overwrites_when_present():
    table = _table()
    table.put({"key": "widget", "name": "Widget"})
    table.put({"key": "widget", "name": "Widget V2"})
    assert table.get("widget") == {"key": "widget", "name": "Widget V2"}


@requires_postgres
def test_update_merges_fields_into_existing_record():
    table = _table()
    table.put({"key": "widget", "name": "Widget", "clicked": 0})
    table.update({"clicked": 5}, "widget")
    assert table.get("widget") == {"key": "widget", "name": "Widget", "clicked": 5}


@requires_postgres
def test_update_missing_key_returns_none():
    table = _table()
    assert table.update({"clicked": 5}, "does-not-exist") is None


@requires_postgres
def test_delete_removes_the_record():
    table = _table()
    table.put({"key": "widget", "name": "Widget"})
    table.delete("widget")
    assert table.get("widget") is None


@requires_postgres
def test_fetch_returns_all_records_in_the_collection():
    table = _table()
    table.put({"key": "a", "name": "A"})
    table.put({"key": "b", "name": "B"})
    names = sorted(item["name"] for item in table.fetch().items)
    assert names == ["A", "B"]


@requires_postgres
def test_fetch_does_not_see_other_collections():
    table_a = _table()
    table_b = _table()
    table_a.put({"key": "x", "name": "In A"})
    assert table_b.fetch().items == []
```

Note: the `requires_postgres` marker is defined once here and reused (imported, not redefined) by later tasks' tests that also construct a `KVTable`/`DETA` instance (Task 4). Task 3's `LocalDrive` tests need no such marker — they never touch Postgres.

- [ ] **Step 2: Run the tests to verify they fail**

Run: `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres pytest backend/data/test_database.py -v`
Expected: FAIL with `ImportError: cannot import name 'KVTable' from 'backend.data.database'` (it doesn't exist yet).

- [ ] **Step 3: Implement `FetchResult` and `KVTable`**

In `backend/data/database.py`, directly below the `get_connection` function from Task 1, add:

```python
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
```

Note why the connection uses `autocommit=True` (set in Task 1's `get_connection`): without it, a failed `insert()` on a duplicate key leaves the connection's transaction in an aborted state, and every subsequent query on that same connection fails with "current transaction is aborted" until an explicit rollback. Autocommit makes each statement its own transaction, so a caught `insert()` failure never poisons later calls — this is exactly what `test_insert_duplicate_key_does_not_break_the_connection` checks.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres pytest backend/data/test_database.py -v`
Expected: all `test_*` in the file PASS.

- [ ] **Step 5: Run the full CI-equivalent lint + test check to confirm nothing else breaks**

Run: `python3 -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics && pytest`
Expected: flake8 prints `0`; `pytest` passes (with `backend/data/test_database.py` tests skipped, since `DATABASE_URL` isn't set in that second command — this mirrors what CI will see).

- [ ] **Step 6: Commit**

```bash
git add backend/data/database.py backend/data/test_database.py
git commit -m "feat: add Postgres-backed KVTable replacing Deta Base"
```

---

### Task 3: `LocalDrive` — disk-backed replacement for Deta Drive

**Files:**
- Modify: `backend/data/database.py` (add `LocalDrive` and `_DriveFile` classes, add `get_drive()` helper)
- Test: `backend/data/test_database.py` (append tests)

**Interfaces:**
- Produces: `LocalDrive(root: str)` with `put(path: str, data: bytes) -> str`, `get(path: str) -> _DriveFile | None` (where `_DriveFile.read() -> bytes`), `delete(path: str) -> None`, `list() -> {"names": list[str]}`. `get_drive() -> LocalDrive` reads its root from `IMAGE_STORAGE_PATH` (default `./local_images`).

This task exists specifically to cover a latent bug: the app writes images with `self.drive.put(f'{catalog_name}/{image_name}', ...)` (no leading slash, in `backend/data/item.py`) but reads them with `self.drive.get(f"/{catalog}/{name}")` (leading slash, in `database.py`). Under the real Deta Drive SDK these likely resolved to the same object; `LocalDrive` must normalize leading slashes so `put` and `get` agree on the same file path.

- [ ] **Step 1: Write the failing tests**

Append to `backend/data/test_database.py`:

```python
from backend.data.database import LocalDrive


def _drive(tmp_path) -> LocalDrive:
    return LocalDrive(root=str(tmp_path))


def test_put_then_get_returns_the_bytes(tmp_path):
    drive = _drive(tmp_path)
    drive.put("Catalog Name/photo.png", b"image-bytes")
    assert drive.get("Catalog Name/photo.png").read() == b"image-bytes"


def test_get_missing_path_returns_none(tmp_path):
    drive = _drive(tmp_path)
    assert drive.get("nope.png") is None


def test_put_without_leading_slash_is_readable_with_leading_slash(tmp_path):
    drive = _drive(tmp_path)
    drive.put("Catalog/photo.png", b"image-bytes")
    assert drive.get("/Catalog/photo.png").read() == b"image-bytes"


def test_delete_removes_the_file(tmp_path):
    drive = _drive(tmp_path)
    drive.put("Catalog/photo.png", b"image-bytes")
    drive.delete("/Catalog/photo.png")
    assert drive.get("Catalog/photo.png") is None


def test_list_returns_relative_paths_of_all_files(tmp_path):
    drive = _drive(tmp_path)
    drive.put("Catalog A/one.png", b"1")
    drive.put("Catalog B/two.png", b"2")
    names = sorted(drive.list()["names"])
    assert names == ["Catalog A/one.png", "Catalog B/two.png"]
```

Note these tests use pytest's built-in `tmp_path` fixture (not `DATABASE_URL`), so they are not skipped — `LocalDrive` needs no live Postgres to test.

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest backend/data/test_database.py -k LocalDrive -v` (this won't match anything yet by name — instead run: `pytest backend/data/test_database.py -v` and look for the new `test_put_then_get...` etc.)
Expected: FAIL with `ImportError: cannot import name 'LocalDrive' from 'backend.data.database'`.

- [ ] **Step 3: Implement `LocalDrive`, `_DriveFile`, and `get_drive`**

In `backend/data/database.py`, below `KVTable` and above `class DETA:`, add:

```python
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest backend/data/test_database.py -v`
Expected: the new `LocalDrive` tests PASS. The earlier `KVTable` tests show as SKIPPED if `DATABASE_URL` isn't set in this shell (each is individually decorated with `@requires_postgres`, not a module-wide marker, so this skip never touches the `LocalDrive` tests) — that's expected, not a failure. If `DATABASE_URL` is set, the `KVTable` tests PASS too.

- [ ] **Step 5: Commit**

```bash
git add backend/data/database.py backend/data/test_database.py
git commit -m "feat: add LocalDrive replacing Deta Drive, normalize leading-slash paths"
```

---

### Task 4: Rewire the `DETA` base class onto `KVTable`/`LocalDrive`

**Files:**
- Modify: `backend/data/database.py` (replace the body of `class DETA:`)
- Test: `backend/data/test_database.py` (append an integration test)

**Interfaces:**
- Consumes: `KVTable` (Task 2), `LocalDrive`/`get_drive()` (Task 3)
- Produces: `DETA(db: str)` with the same public surface the six subclasses already call: `self.db` (a `KVTable`), `self.drive` (a `LocalDrive`), and methods `fetch_records()`, `get_record(key)`, `get_image_data(name, catalog)`, `del_image_data(name, catalog)`, `get_image_names()`, `get_record_by_catalog(catalog)`, `update_record(key, updates)`, `add_new_attribute(key, new_attr)`, `change_record(key, updates)`, `delete_item(key)`, `migrate_database(target_database)`.

Two methods need real logic changes, not just a swap of what's underneath, because they reached into Deta's client directly instead of going through `self.db`/`self.drive`:

- `delete_item` called `self.deta.Base("catalog_db")` directly (there's no more `self.deta` client object) — replace with `KVTable(collection="catalog_db", conn=self.db.conn)`.
- `migrate_database` called `self.deta.Base(target_database)` the same way — same replacement, reusing `self.db.conn` so it's the same live connection.

`add_new_attribute` and `change_record` have no callers anywhere in the codebase (verified by grep) — leave their bodies exactly as they are; they're out of scope for this migration.

- [ ] **Step 1: Write the failing integration test**

Append to `backend/data/test_database.py`:

```python
from backend.data.database import DETA


@requires_postgres
def test_deta_class_full_lifecycle_against_a_real_backend():
    db_name = f"test_{uuid.uuid4().hex}"
    backup_name = f"{db_name}_backup"
    deta = DETA(db=db_name)

    deta.db.insert({"key": "widget", "name": "Widget", "catalog": "Tools"})
    assert deta.get_record("widget") == {
        "key": "widget", "name": "Widget", "catalog": "Tools",
    }
    assert deta.fetch_records() == [
        {"key": "widget", "name": "Widget", "catalog": "Tools"},
    ]
    assert deta.get_record_by_catalog("Tools") == [
        {"key": "widget", "name": "Widget", "catalog": "Tools"},
    ]

    deta.update_record(key="widget", updates={"catalog": "Hardware"})
    assert deta.get_record("widget")["catalog"] == "Hardware"

    deta.migrate_database(backup_name)
    backup = DETA(db=backup_name)
    assert backup.get_record("widget")["catalog"] == "Hardware"

    deta.delete_item(key="widget")
    assert deta.get_record("widget") is None


@requires_postgres
def test_deta_class_image_roundtrip(tmp_path, monkeypatch):
    # DETA.__init__ always opens a real Postgres connection via get_connection(),
    # even though this test only exercises the drive — so it needs the marker too.
    monkeypatch.setenv("IMAGE_STORAGE_PATH", str(tmp_path))
    deta = DETA(db=f"test_{uuid.uuid4().hex}")

    deta.drive.put("Tools/widget.png", b"image-bytes")
    assert deta.get_image_data("widget.png", "Tools") == b"image-bytes"

    deta.del_image_data("widget.png", "Tools")
    assert deta.drive.get("Tools/widget.png") is None
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres pytest backend/data/test_database.py -v -k test_deta_class`
Expected: FAIL — `DETA.__init__` still has its original body (`self.deta = Deta(os.getenv("DETA_KEY"))`), and Task 1 already removed the `from deta import Deta` import, so this raises `NameError: name 'Deta' is not defined`.

- [ ] **Step 3: Rewrite `class DETA:`**

Replace the entire `class DETA:` block in `backend/data/database.py` (from `class DETA:` down to — but not including — the `if __name__ == '__main__':` block at the bottom) with:

```python
class DETA:

    def __init__(self, db: str) -> None:
        self.db_name = db
        self.db = KVTable(collection=db, conn=get_connection())
        self.drive = get_drive()

    def fetch_records(self) -> list:
        return self.db.fetch().items

    def get_record(self, key: str):
        return self.db.get(key)

    def get_image_data(self, name: str, catalog: str) -> bytes:
        return self.drive.get(f"/{catalog}/{name}").read()

    def del_image_data(self, name: str, catalog: str) -> None:
        return self.drive.delete(f"/{catalog}/{name}")

    def get_image_names(self):
        return self.drive.list()['names']

    def get_record_by_catalog(self, catalog: str) -> list:
        records = self.fetch_records()
        return [record for record in records if catalog == record['catalog']]

    def update_record(self, key: str, updates: dict):
        record = self.db.get(key)
        for k, v in updates.items():
            if k in record:
                record[k] = v
        try:
            logging.info(f'Updated: {key}')
            return self.db.put(record)
        except Exception as e:
            logging.error(f'Error in Updating: {key} ---> {e}')

    def add_new_attribute(self, key: str, new_attr: dict):
        attributes = self.db.get(key)
        attributes.update(new_attr)
        self.db.put(attributes)

    def change_record(self, key: str, updates: dict) -> str:
        record = self.db.get(key)
        for k, v in updates.items():
            if k in record:
                record[k] = v

        self.delete_item(key)
        if 'name' in record:
            record['key'] = record['name'].replace(' ', '_')

        self.db.put(record)

        logging.info(f"{key} successfully changed record.")
        return f"{key} successfully changed record."

    def delete_item(self, key: str):
        name = key
        key = key.replace(' ', '_')
        try:
            catalog_name = self.get_record(key)['catalog']
            catalog_table = KVTable(collection="catalog_db", conn=self.db.conn)
            catalog_record = catalog_table.get(catalog_name)
            for item in catalog_record['item_list']:
                if item == name:
                    catalog_record['item_list'].remove(item)
                    break
            catalog_table.put(catalog_record)
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
        target = KVTable(collection=target_database, conn=self.db.conn)
        for item in self.db.fetch().items:
            if not item['key'].startswith('Corsair'):
                try:
                    target.put(item)
                    logging.info('%s is migrated!', item["key"])
                except Exception as e:
                    logging.error('Error migrating %s --> %s', item["key"], e)
                    raise e
        return
```

Two intentional fixes made while rewriting (both were pre-existing bugs, now corrected since the method bodies were being touched anyway):
- `add_new_attribute` previously called `self.db.put(key=key, data=new_attr)`, which matched the real Deta SDK's signature but would `TypeError` against `KVTable.put(self, data)`. Fixed to fetch-merge-put like the rest of the class (it has no callers, so this is a safety net, not a behavior change anyone depends on).
- `get_record`/`get_image_data`/etc. drop the `# type: ignore` comments that were silencing type errors specific to the old Deta SDK's untyped return values — no longer needed since `KVTable`/`LocalDrive` are typed.

Also replace the file's `if __name__ == '__main__':` block at the bottom (it references `del_image_data` directly on a throwaway `DETA('item_db2')` instance — keep it, no change needed, it already matches the new interface) — leave it as-is:

```python
if __name__ == '__main__':
    DETA('item_db2').del_image_data(
        name='Nathan Running Handheld Quick Squeeze.jpeg', catalog='Water Bottle')
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres pytest backend/data/test_database.py -v`
Expected: every test in the file PASSES, including `test_deta_class_full_lifecycle_against_a_real_backend` and `test_deta_class_image_roundtrip`.

- [ ] **Step 5: Run the CI-equivalent checks**

Run: `python3 -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics && python3 -m py_compile backend/data/database.py`
Expected: flake8 prints `0`; compile succeeds with no output.

- [ ] **Step 6: Commit**

```bash
git add backend/data/database.py backend/data/test_database.py
git commit -m "feat: rewire DETA base class onto KVTable/LocalDrive"
```

---

### Task 5: Point `send_email.py` at the shared shim

**Files:**
- Modify: `backend/email/send_email.py:1-29`

**Interfaces:**
- Consumes: `KVTable`, `get_connection`, `get_drive` (from `backend.data.database`, Tasks 2–3)

`send_email.py` currently opens its own separate `Deta(os.getenv("DETA_KEY"))` connection instead of going through `database.py`. This task points it at the same primitives so there's one source of truth for storage config, without changing any of its business logic (`get_subscription_list`, `get_item`, `get_image`, `send_email`).

- [ ] **Step 1: Replace the Deta import and client setup**

In `backend/email/send_email.py`, replace lines 1–22:

```python
import base64
import logging
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path

from deta import Deta
from dotenv import load_dotenv

from frontend.utils.utils import get_img_with_href

ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

DETA = Deta(os.getenv("DETA_KEY"))
```

with:

```python
import base64
import logging
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv

from backend.data.database import KVTable, get_connection, get_drive
from frontend.utils.utils import get_img_with_href

ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()
```

- [ ] **Step 2: Update `connect_db` and `get_image`**

Replace:
```python
    @staticmethod
    def connect_db(db: str):
        return DETA.Base(db)
```
with:
```python
    @staticmethod
    def connect_db(db: str):
        return KVTable(collection=db, conn=get_connection())
```

Replace:
```python
    @staticmethod
    def get_image(catalog: str, name: str):
        return DETA.Drive('images_db').get(f"/{catalog}/{name}").read()
```
with:
```python
    @staticmethod
    def get_image(catalog: str, name: str):
        return get_drive().get(f"/{catalog}/{name}").read()
```

Nothing else in the file changes — `get_subscription_list`, `get_item`, and `send_email` all call `connect_db(...)`/`get_image(...)` the same way as before, and `KVTable.get(key=key)` / `.fetch().items` support the same keyword/attribute usage those methods already use.

- [ ] **Step 3: Verify it compiles and imports cleanly**

Run: `python3 -m py_compile backend/email/send_email.py`
Expected: no output (success).

Run:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres python3 -c "
from backend.email.send_email import EmailService
print(EmailService.get_subscription_list())
"
```
Expected: prints `[]` (empty list — no subscribers exist yet in the fresh database) without raising.

- [ ] **Step 4: Run the CI-equivalent lint check**

Run: `python3 -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
Expected: `0`

- [ ] **Step 5: Commit**

```bash
git add backend/email/send_email.py
git commit -m "refactor: point send_email.py at the shared database shim instead of its own Deta client"
```

---

### Task 6: Seed the first admin login

**Files:**
- Create: `scripts/seed_admin.py`

**Interfaces:**
- Consumes: `backend.data.admin.Admin` (unchanged, now backed by the new `DETA`/`KVTable` from Task 4)

There's no UI anywhere that calls `Admin.create_user` — nothing creates the first admin login. With Deta's old data gone, `admin_db` starts empty, which would permanently lock `pages/admin.py` (it's gated by `auth()` in `frontend/utils/auth.py`, which reads credentials from `admin_db` via `Admin().fetch_records()`). This is a one-off script, run once against the production database after deploy, not part of the app's runtime code path.

- [ ] **Step 1: Check `Admin.create_user`'s exact contract**

Re-read `backend/data/admin.py` (already present, unchanged by this migration):
```python
def create_user(self, name: str, username: str, password: str):
    if not self._validate_username(username):
        raise ValueError("Invalid email address")
    self.name = name
    self.key = username
    self.password = password
```
Note: `create_user` only sets attributes on the `Admin` instance — it does **not** call `self.db.insert(...)` or `self.db.put(...)` itself. The seed script must persist the record explicitly.

Also note `frontend/utils/auth.py` expects each record from `Admin().fetch_records()` to have `cred['name']`, `cred['key']`, `cred['password']` — and it hashes `password` at login time via `stauth.Hasher(passwords).generate()`, so the seed script must store the **plaintext** password (the hashing happens at login, not at storage time — this matches how the rest of the app already behaves, not a new decision).

- [ ] **Step 2: Write the script**

Create `scripts/seed_admin.py`:

```python
"""One-off script: seed the first admin login into admin_db.

Run once after deploying against a fresh database:
    DATABASE_URL=... python3 scripts/seed_admin.py <name> <username> <password>
"""
import sys

from backend.data.admin import Admin


def main():
    if len(sys.argv) != 4:
        print("usage: seed_admin.py <name> <username> <password>")
        sys.exit(1)

    name, username, password = sys.argv[1], sys.argv[2], sys.argv[3]

    admin = Admin()
    admin.create_user(name=name, username=username, password=password)
    admin.db.insert({"key": admin.key, "name": admin.name, "password": admin.password})
    print(f"Seeded admin user: {username}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run it against the local test Postgres and verify**

Run:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres \
  python3 scripts/seed_admin.py "Serhan Sari" admin correct-horse-battery-staple
```
Expected: prints `Seeded admin user: admin`.

Verify the record is there and shaped the way `auth.py` expects:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres python3 -c "
from backend.data.admin import Admin
print(Admin().fetch_records())
"
```
Expected: `[{'key': 'admin', 'name': 'Serhan Sari', 'password': 'correct-horse-battery-staple'}]`

- [ ] **Step 4: Run it a second time to confirm it fails loudly on a duplicate username instead of silently corrupting state**

Run the same seed command again with the same username.
Expected: raises (uncaught `Exception` from `KVTable.insert`'s duplicate-key `INSERT`) rather than silently succeeding or overwriting — this is intentional; re-running the script for a username that already exists should not go unnoticed.

- [ ] **Step 5: Commit**

```bash
git add scripts/seed_admin.py
git commit -m "chore: add one-off script to seed the first admin login"
```

---

## Post-plan manual steps (not code — do these once, in Railway, after Task 6 lands)

1. Add the Postgres plugin to the Railway project and link it to the app service (Railway sets `DATABASE_URL` automatically).
2. Add a Volume to the app service, mount it at e.g. `/data/images`, and set `IMAGE_STORAGE_PATH=/data/images` in the service's environment variables.
3. Deploy.
4. Run `scripts/seed_admin.py` once against production (e.g. via `railway run python3 scripts/seed_admin.py ...`) to create the first admin login.
