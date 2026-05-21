import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile, status

from .database.db import PostCollection, UserCollection

CURRENT_USER_ID = os.getenv("CURRENT_USER_ID", "sakura_art")
UPLOAD_ROOT = Path(__file__).resolve().parents[1] / "uploads" / "posts"
ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}

router = APIRouter()


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def to_iso(value) -> str:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat()
    if value:
        return str(value)
    return now_utc().isoformat()


def fallback_account() -> dict:
    now = now_utc()
    return {
        "id": CURRENT_USER_ID,
        "username": CURRENT_USER_ID,
        "email": "sakura@example.jp",
        "displayName": "さくら",
        "bio": "画像SNSのデモアカウントです。",
        "avatarUrl": None,
        "createdAt": now,
        "updatedAt": now,
    }


def normalize_account(user: Optional[dict]) -> dict:
    user = user or fallback_account()
    user_id = user.get("id") or user.get("user_id") or user.get("username") or CURRENT_USER_ID
    username = user.get("username") or user.get("user_id") or user_id

    return {
        "id": user_id,
        "username": username,
        "email": user.get("email") or f"{username}@example.jp",
        "displayName": user.get("displayName") or user.get("display_name") or username,
        "bio": user.get("bio"),
        "avatarUrl": user.get("avatarUrl") or user.get("icon_url"),
        "createdAt": to_iso(user.get("createdAt") or user.get("created_at")),
    }


def get_current_account() -> dict:
    user = UserCollection.find_one(
        {"$or": [{"id": CURRENT_USER_ID}, {"username": CURRENT_USER_ID}, {"user_id": CURRENT_USER_ID}]}
    )

    if user is None:
        default_user = fallback_account()
        UserCollection.update_one({"id": CURRENT_USER_ID}, {"$setOnInsert": default_user}, upsert=True)
        user = default_user

    return normalize_account(user)


def get_account_by_id(account_id: str) -> dict:
    user = UserCollection.find_one(
        {"$or": [{"id": account_id}, {"username": account_id}, {"user_id": account_id}]}
    )
    return normalize_account(user)


def normalize_post(post: dict) -> dict:
    post_id = post.get("id") or post.get("post_id") or str(post.get("_id"))
    account_id = post.get("accountId") or post.get("author_id") or CURRENT_USER_ID
    image_url = post.get("imageUrl")

    if not image_url:
        image_urls = post.get("image_urls") or []
        image_url = image_urls[0] if image_urls else ""

    return {
        "id": post_id,
        "text": post.get("text") or post.get("detail") or post.get("title") or "",
        "imageUrl": image_url,
        "createdAt": to_iso(post.get("createdAt") or post.get("created_at")),
        "account": normalize_account(post.get("account") or get_account_by_id(account_id)),
        "likes": int(post.get("likes", 0)),
        "comments": int(post.get("comments", 0)),
    }


def save_image(post_id: str, image: UploadFile) -> str:
    content_type = image.content_type or ""
    extension = ALLOWED_IMAGE_TYPES.get(content_type)

    if extension is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, WEBP, and GIF images are allowed.",
        )

    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    filename = f"{post_id}{extension}"
    file_path = UPLOAD_ROOT / filename

    with file_path.open("wb") as out_file:
        out_file.write(image.file.read())

    return f"/uploads/posts/{filename}"


@router.get("")
@router.get("/")
def list_posts(
    limit: int = Query(default=5, ge=1, le=30),
    cursor: Optional[str] = Query(default=None),
):
    start = int(cursor or 0)
    docs = list(PostCollection.find({}).sort("createdAt", -1).skip(start).limit(limit + 1))
    visible_docs = docs[:limit]
    next_index = start + len(visible_docs)

    return {
        "posts": [normalize_post(post) for post in visible_docs],
        "nextCursor": str(next_index) if len(docs) > limit else None,
        "hasMore": len(docs) > limit,
    }


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(text: str = Form(...), image: UploadFile = File(...)):
    clean_text = text.strip()

    if not clean_text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text is required.")

    account = get_current_account()
    post_id = str(uuid4())
    image_url = save_image(post_id, image)
    now = now_utc()
    post_doc = {
        "id": post_id,
        "text": clean_text,
        "imageUrl": image_url,
        "accountId": account["id"],
        "likes": 0,
        "comments": 0,
        "createdAt": now,
        "updatedAt": now,
    }

    PostCollection.insert_one(post_doc)
    return normalize_post(post_doc)


@router.get("/{post_id}")
def get_post(post_id: str):
    post = PostCollection.find_one({"$or": [{"id": post_id}, {"post_id": post_id}]})

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

    return normalize_post(post)


def list_current_user_posts() -> list[dict]:
    account = get_current_account()
    docs = list(
        PostCollection.find({"$or": [{"accountId": account["id"]}, {"author_id": account["id"]}]}).sort(
            "createdAt", -1
        )
    )
    return [normalize_post(post) for post in docs]
