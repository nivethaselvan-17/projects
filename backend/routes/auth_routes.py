"""Routes for user signup/login."""
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from auth import hash_password, verify_password, create_access_token
from database import get_database
from models.schemas import UserSignup, UserLogin, TokenResponse, UserPublic


router = APIRouter(tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(payload: UserSignup):
    db = get_database()

    existing = db.users.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user_id = str(uuid4())
    user_doc = {
        "_id": user_id,
        "name": payload.name,
        "email": payload.email,
        "password": hash_password(payload.password),
    }
    db.users.insert_one(user_doc)

    token = create_access_token(user_id)
    return TokenResponse(access_token=token, user=UserPublic(id=user_id, name=payload.name, email=payload.email))


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin):
    db = get_database()

    user = db.users.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(user["_id"])
    return TokenResponse(
        access_token=token,
        user=UserPublic(id=user["_id"], name=user["name"], email=user["email"]),
    )
