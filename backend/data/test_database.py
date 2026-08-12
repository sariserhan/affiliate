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

    catalog_key = f"test_cat_{uuid.uuid4().hex}"
    catalog_table = KVTable(collection="catalog_db", conn=deta.db.conn)
    try:
        deta.update_record(key="widget", updates={"catalog": catalog_key})
        assert deta.get_record("widget")["catalog"] == catalog_key

        deta.migrate_database(backup_name)
        backup = DETA(db=backup_name)
        assert backup.get_record("widget")["catalog"] == catalog_key

        # delete_item looks up the catalog record in the shared "catalog_db"
        # collection and removes the item from its item_list. It matches on
        # item == name, where name is the original (unmodified) key argument
        # passed to delete_item below, i.e. "widget".
        catalog_table.put({
            "key": catalog_key, "name": catalog_key, "is_active": True,
            "item_list": ["widget"],
        })

        deta.delete_item(key="widget")
        assert deta.get_record("widget") is None
        assert catalog_table.get(catalog_key)["item_list"] == []
    finally:
        catalog_table.delete(catalog_key)


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
