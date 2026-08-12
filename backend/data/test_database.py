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
