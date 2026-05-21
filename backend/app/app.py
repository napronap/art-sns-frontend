from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database.db import ensure_indexes
from .posts import get_current_account, list_current_user_posts, router as posts_router
from .users import router as users_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(posts_router, prefix="/api/posts", tags=["posts"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


@app.on_event("startup")
async def startup_event() -> None:
    ensure_indexes()


@app.get("/")
def root():
    return {"message": "Art SNS API"}


@app.get("/api/me")
def read_current_account():
    return get_current_account()


@app.get("/api/me/posts")
def read_current_account_posts():
    return list_current_user_posts()
