from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from .database.db import UserCollection
from .schemas import (
    ProfileUpdate,
    TokenResponse,
    UserLogin,
    UserProfile,
    UserRegister,
)

SECRET_KEY = "CHANGE_THIS_SECRET_KEY_TO_A_RANDOM_VALUE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter()


def get_user(user_id: str) -> Optional[dict]:
    return UserCollection.find_one(
        {"$or": [{"user_id": user_id}, {"id": user_id}, {"username": user_id}]}
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(user_id: str, password: str) -> Optional[dict]:
    user = get_user(user_id)
    if not user:
        return None
    if not user.get("password_hash") or not verify_password(password, user["password_hash"]):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(user_id)
    if user is None:
        raise credentials_exception
    return user


def format_profile(user: dict) -> UserProfile:
    user_id = user.get("user_id") or user.get("id") or user.get("username")
    created_at = user.get("created_at") or user.get("createdAt") or datetime.utcnow()
    updated_at = user.get("updated_at") or user.get("updatedAt") or created_at

    return UserProfile(
        user_id=user_id,
        display_name=user.get("display_name") or user.get("displayName") or user_id,
        icon_url=user.get("icon_url") or user.get("avatarUrl"),
        bio=user.get("bio"),
        created_at=created_at,
        updated_at=updated_at,
    )


@router.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegister):
    existing = get_user(payload.user_id)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID already exists")

    password_hash = get_password_hash(payload.password)
    now = datetime.utcnow()

    user_doc = {
        "id": payload.user_id,
        "username": payload.user_id,
        "user_id": payload.user_id,
        "email": f"{payload.user_id}@example.jp",
        "password_hash": password_hash,
        "displayName": payload.user_id,
        "display_name": payload.user_id,
        "avatarUrl": None,
        "icon_url": None,
        "bio": None,
        "createdAt": now,
        "updatedAt": now,
        "created_at": now,
        "updated_at": now,
    }
    UserCollection.insert_one(user_doc)
    return format_profile(user_doc)


@router.post("/login", response_model=TokenResponse)
def login_user(payload: UserLogin):
    user = authenticate_user(payload.user_id, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})

    access_token = create_access_token(data={"sub": user.get("user_id") or user.get("id")})
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserProfile)
async def read_own_profile(current_user: dict = Depends(get_current_user)):
    return format_profile(current_user)


@router.patch("/me/profile", response_model=UserProfile)
async def update_profile(payload: ProfileUpdate, current_user: dict = Depends(get_current_user)):
    update_data = {}
    if payload.display_name is not None:
        update_data["display_name"] = payload.display_name
        update_data["displayName"] = payload.display_name
    if payload.icon_url is not None:
        update_data["icon_url"] = payload.icon_url
        update_data["avatarUrl"] = payload.icon_url
    if payload.bio is not None:
        update_data["bio"] = payload.bio
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No profile fields provided")

    update_data["updated_at"] = datetime.utcnow()
    update_data["updatedAt"] = update_data["updated_at"]
    current_user_id = current_user.get("user_id") or current_user.get("id")
    UserCollection.update_one(
        {"$or": [{"user_id": current_user_id}, {"id": current_user_id}]},
        {"$set": update_data},
    )
    current_user.update(update_data)
    return format_profile(current_user)


@router.get("/{user_id}", response_model=UserProfile)
def read_user_profile(user_id: str):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return format_profile(user)
