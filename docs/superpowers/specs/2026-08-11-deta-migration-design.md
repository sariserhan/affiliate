# Migrate off Deta Base/Drive to Railway Postgres + Volume

## Background

The app's entire data layer (`backend/data/catalog.py`, `item.py`, `category.py`,
`subscribe.py`, `affiliate_partner.py`, `admin.py`) inherits from a `DETA` base
class in `backend/data/database.py` that wraps `deta.Deta().Base()` (key-value
document store) and `.Drive()` (blob storage). `backend/email/send_email.py`
also opens its own separate `Deta(...)` connection for the same Drive.

Deta Base/Space has been retired. Separately, `requirements.txt` pins
`deta==1.2.0`, which never existed on PyPI (latest real release is `0.2.53`),
and the `deta` package name on PyPI has since been taken over by an unrelated,
anonymously-published "infrastructure anomaly detection" tool with no `Deta`/
`Base`/`Drive` classes at all. So this isn't a version-pin fix — the real SDK
is gone and the service behind it is gone too. The user confirmed:

- Deta account/data is already unreachable — no export needed, starting fresh.
- Production runs on Railway (PaaS, ephemeral filesystem unless a Volume is
  attached).
- Railway is the existing provider to build against (no Supabase/other vendor).

## Goals

- Get the app running again on infrastructure the user already has (Railway).
- Preserve existing application code/behavior in `backend/data/*.py` as much
  as possible — this is an infra swap, not a data-model redesign.
- Minimal new dependencies and moving parts.

## Non-goals

- Redesigning the data model into a normalized relational schema (separate
  `items`/`catalogs`/`categories` tables with foreign keys). The current model
  is a set of documents with array-of-name relations (e.g. a catalog document
  holds an `item_list` of item names). That's a legitimate future project but
  is out of scope here — the goal is restoring a working backend, not a
  schema redesign.
- Recovering old Deta data. It's confirmed gone.

## Architecture

Replace the `DETA` base class internals in `backend/data/database.py` with a
drop-in shim exposing the same interface every subclass already calls:
`self.db.insert(data)`, `self.db.put(data)`, `self.db.get(key)`,
`self.db.update(updates, key)`, `self.db.delete(key)`, `self.db.fetch().items`,
and `self.drive.put(path, bytes)`, `self.drive.get(path).read()`,
`self.drive.delete(path)`, `self.drive.list()['names']`.

Because the interface doesn't change, `catalog.py`, `item.py`, `category.py`,
`subscribe.py`, `affiliate_partner.py`, and `admin.py` need **no changes**.

### Database: generic KV table in Postgres

```sql
CREATE TABLE kv_store (
    collection text NOT NULL,
    key text NOT NULL,
    data jsonb NOT NULL,
    updated_at timestamptz DEFAULT now(),
    PRIMARY KEY (collection, key)
);
```

Each `DETA(db="items_db2")`-style base becomes rows with
`collection = 'items_db2'`. This preserves the existing document shape
(including array fields like `item_list`, `catalog_list`, `categories`)
without a relational redesign, and needs zero schema migrations when a new
"database" (Deta Base name) is introduced.

Operation mapping:

| DETA/Base call | Postgres shim behavior |
|---|---|
| `insert(data)` | `INSERT INTO kv_store ...` — raises (Postgres `UniqueViolation`, a subclass of `Exception`) on duplicate key, same as Deta's insert. Existing `except Exception:` blocks in `catalog.py`/`category.py`/`affiliate_partner.py`/`item.py` keep working unchanged. |
| `put(data)` | `INSERT ... ON CONFLICT (collection, key) DO UPDATE SET data = ...` (upsert) |
| `get(key)` | `SELECT data FROM kv_store WHERE collection = ... AND key = ...` → dict or `None` |
| `update(updates, key)` | Fetch, merge dict, write back (partial update, matches Deta's `Base.update` signature `update(updates, key)`) |
| `delete(key)` | `DELETE FROM kv_store WHERE collection = ... AND key = ...` |
| `fetch()` | `SELECT data FROM kv_store WHERE collection = ...` → object with `.items` (list of dicts), matching `self.db.fetch().items` usage |

`migrate_database(target_database)` (used by the admin "Settings" backup
buttons) becomes: copy all rows for the current collection into rows under
`collection = target_database`.

### Image storage: Railway Volume

Confirmed every image read in the app goes through
`get_image_data(name, catalog)` → `self.drive.get(...).read()` → raw bytes →
`PIL.Image.open(BytesIO(...))`. Public URLs are never used. A local directory
under a Railway Volume mount is therefore a true drop-in replacement.

`LocalDrive` implements only what's actually called:
- `.put(path, data: bytes)` — write `{IMAGE_STORAGE_PATH}/{path}`, creating
  parent dirs as needed
- `.get(path)` — returns a small wrapper object with `.read()` returning bytes
  (or `None` if missing, matching Deta's not-found behavior)
- `.delete(path)`
- `.list()` — returns `{'names': [...]}` (relative paths under the drive root)

`IMAGE_STORAGE_PATH` env var controls the root directory — set to the Railway
Volume's mount path in production, defaults to a local folder for dev.

### Config changes

- `DETA_KEY` → `DATABASE_URL` (Railway provides this automatically once the
  Postgres plugin is added and linked to the service)
- New env var: `IMAGE_STORAGE_PATH`
- `requirements.txt`: remove `deta==1.2.0`, add `psycopg[binary]` (raw SQL —
  no ORM needed for five generic operations on one table)

### send_email.py

Currently opens its own separate `Deta(os.getenv("DETA_KEY"))` connection to
reach the same Drive. This will be changed to go through the same shim in
`database.py` instead, so there's one source of truth for storage config.

### Admin bootstrap

There is currently no UI path that calls `Admin.create_user` — nothing
creates the first admin login. With Deta's data gone, `admin_db` starts
empty, which would permanently lock `pages/admin.py` (it's gated by
`auth()`, which reads credentials from `admin_db`). A one-off seed script
will insert an initial admin credential row as part of the migration.

## Error handling

- Shim raises the same exception shapes the calling code already expects
  (`Exception` on `insert()` conflict) — no changes needed to existing
  `try/except` blocks in the six `backend/data/*.py` files.
- `get()`/`drive.get()` return `None` on missing key/path, matching current
  Deta semantics (`if not category:` style checks already in the code depend
  on this).
- Connection/config errors (e.g. missing `DATABASE_URL`) should fail loudly
  at startup rather than lazily per-request.

## Testing

The KV shim is the one piece of genuinely branchy new logic (insert-vs-conflict,
upsert, partial update, missing-key handling). Add `backend/data/test_database.py`
with plain `assert`-based checks (no framework) exercising insert / get / put /
update / delete / fetch against a real Postgres reachable via `DATABASE_URL`
(local Postgres or the Railway dev database both work). No per-function test
suite beyond this — the six data-model files are unchanged, so they're covered
by the fact that the shim honors the same contract they already rely on.

## Explicit simplifications (ponytail)

- KV-over-Postgres instead of a normalized relational schema — upgrade path
  if query complexity or reporting needs grow.
- Single generic `kv_store` table instead of one table per collection — keeps
  adding new "databases" a zero-migration change; revisit if per-collection
  indexing/constraints become necessary.
