from os import environ, getenv
from pathlib import Path

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


def load_local_env() -> None:
    backend_dir = Path(__file__).resolve().parents[2]
    project_dir = backend_dir.parent

    for env_path in (project_dir / ".env", backend_dir / ".env"):
        if not env_path.exists():
            continue

        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key:
                environ.setdefault(key, value)


load_local_env()

MONGO_URI = getenv(
    "MONGO_URI",
    "mongodb+srv://tcapg22503018_Haruki:rubiyan191710_Hse@cluster0.4qkhd3p.mongodb.net/?appName=Cluster0",
)
MONGO_DB_NAME = getenv("MONGO_DB_NAME", "260521")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[MONGO_DB_NAME]

UserCollection = db["user"]
PostCollection = db["post"]


def ensure_indexes() -> None:
    try:
        UserCollection.create_index("id", unique=True, sparse=True)
        UserCollection.create_index("username", unique=True, sparse=True)
        UserCollection.create_index("user_id", unique=True, sparse=True)
        PostCollection.create_index([("createdAt", -1)])
        PostCollection.create_index([("accountId", 1), ("createdAt", -1)])
    except ServerSelectionTimeoutError:
        pass
