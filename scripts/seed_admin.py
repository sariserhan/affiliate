"""One-off script: seed the first admin login into admin_db.

Run once after deploying against a fresh database:
    DATABASE_URL=... python3 scripts/seed_admin.py <name> <username> <password>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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
