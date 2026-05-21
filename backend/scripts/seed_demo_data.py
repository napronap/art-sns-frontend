from datetime import datetime, timedelta, timezone
from os import getenv

from pymongo import MongoClient, UpdateOne

MONGO_URI = getenv("MONGO_URI")
MONGO_DB_NAME = getenv("MONGO_DB_NAME", "260521")

if not MONGO_URI:
    raise SystemExit("Set MONGO_URI before running this script.")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
db = client[MONGO_DB_NAME]
users = db["user"]
posts = db["post"]

now = datetime.now(timezone.utc)

seed_users = [
    {
        "id": "sakura_art",
        "username": "sakura_art",
        "email": "sakura@example.jp",
        "displayName": "さくら",
        "bio": "日々のイラストを投稿しています。",
        "avatarUrl": None,
        "createdAt": now - timedelta(days=30),
        "updatedAt": now,
    },
    {
        "id": "yuki_photo",
        "username": "yuki_photo",
        "email": "yuki@example.jp",
        "displayName": "ゆき",
        "bio": "写真と構図の練習用アカウントです。",
        "avatarUrl": None,
        "createdAt": now - timedelta(days=24),
        "updatedAt": now,
    },
    {
        "id": "aoi_sketch",
        "username": "aoi_sketch",
        "email": "aoi@example.jp",
        "displayName": "あおい",
        "bio": "ラフスケッチを中心に投稿します。",
        "avatarUrl": None,
        "createdAt": now - timedelta(days=18),
        "updatedAt": now,
    },
]

seed_posts = [
    {
        "id": "seed-post-001",
        "accountId": "sakura_art",
        "text": "新しい作品の色味を試しています。",
        "imageUrl": "https://picsum.photos/seed/jp-art-001/900/900",
        "likes": 14,
        "comments": 2,
        "createdAt": now - timedelta(hours=1),
        "updatedAt": now - timedelta(hours=1),
    },
    {
        "id": "seed-post-002",
        "accountId": "yuki_photo",
        "text": "朝の光で撮った参考写真です。",
        "imageUrl": "https://picsum.photos/seed/jp-art-002/900/900",
        "likes": 9,
        "comments": 1,
        "createdAt": now - timedelta(hours=3),
        "updatedAt": now - timedelta(hours=3),
    },
    {
        "id": "seed-post-003",
        "accountId": "aoi_sketch",
        "text": "人物ラフを少しだけ整理しました。",
        "imageUrl": "https://picsum.photos/seed/jp-art-003/900/900",
        "likes": 21,
        "comments": 4,
        "createdAt": now - timedelta(hours=6),
        "updatedAt": now - timedelta(hours=6),
    },
    {
        "id": "seed-post-004",
        "accountId": "sakura_art",
        "text": "背景の雰囲気を確認中です。",
        "imageUrl": "https://picsum.photos/seed/jp-art-004/900/900",
        "likes": 7,
        "comments": 0,
        "createdAt": now - timedelta(days=1),
        "updatedAt": now - timedelta(days=1),
    },
    {
        "id": "seed-post-005",
        "accountId": "yuki_photo",
        "text": "暗めのトーンで構図をテストしました。",
        "imageUrl": "https://picsum.photos/seed/jp-art-005/900/900",
        "likes": 18,
        "comments": 3,
        "createdAt": now - timedelta(days=2),
        "updatedAt": now - timedelta(days=2),
    },
]

users.bulk_write(
    [
        UpdateOne(
            {"id": user["id"]},
            {"$set": user, "$setOnInsert": {"user_id": user["id"]}},
            upsert=True,
        )
        for user in seed_users
    ]
)
posts.bulk_write([UpdateOne({"id": post["id"]}, {"$set": post}, upsert=True) for post in seed_posts])

users.create_index("id", unique=True, sparse=True)
users.create_index("username", unique=True, sparse=True)
posts.create_index([("createdAt", -1)])
posts.create_index([("accountId", 1), ("createdAt", -1)])

print(f"Seeded {len(seed_users)} users and {len(seed_posts)} posts in {MONGO_DB_NAME}.")
