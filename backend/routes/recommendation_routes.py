"""Recommendation endpoint backed by hybrid ML engine."""
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from auth import get_current_user
from database import get_database
from ml.recommender import build_hybrid_recommendations
from models.schemas import RecommendationResponse, RecommendationOut


router = APIRouter(tags=["recommendations"])
_CACHE: dict[str, dict] = {}
_CACHE_TTL = timedelta(seconds=60)


@router.get("/recommendations/{user_id}", response_model=RecommendationResponse)
def get_recommendations(user_id: str, _: dict = Depends(get_current_user)):
    now = datetime.utcnow()
    cached = _CACHE.get(user_id)
    if cached and now - cached["created_at"] < _CACHE_TTL:
        return cached["payload"]

    db = get_database()
    books = list(db.books.find())
    behaviors = list(db.behaviors.find())

    recs = build_hybrid_recommendations(user_id=user_id, books=books, behaviors=behaviors, top_n=5)
    payload = RecommendationResponse(
        user_id=user_id,
        recommendations=[RecommendationOut(**r.__dict__) for r in recs],
    )
    _CACHE[user_id] = {"created_at": now, "payload": payload}
    return payload
