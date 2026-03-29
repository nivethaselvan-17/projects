"""Pydantic schemas used by the API routes."""
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class UserSignup(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: str
    name: str
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    description: str


class BookOut(BaseModel):
    id: str
    title: str
    author: str
    genre: str
    description: str


class BehaviorTrack(BaseModel):
    user_id: str
    book_id: str
    time_spent_minutes: float = Field(..., ge=0)
    pages_read: int = Field(..., ge=0)
    click_frequency: int = Field(..., ge=0)
    liked: bool = False
    saved: bool = False


class RecommendationOut(BaseModel):
    book_id: str
    title: str
    author: str
    score: float
    reasons: List[str]


class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[RecommendationOut]
