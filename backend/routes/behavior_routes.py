"""Routes for behavior tracking."""
from uuid import uuid4

from fastapi import APIRouter, Depends

from auth import get_current_user
from database import get_database
from models.schemas import BehaviorTrack


router = APIRouter(tags=["behavior"])


@router.post("/track-behavior")
def track_behavior(payload: BehaviorTrack, _: dict = Depends(get_current_user)):
    db = get_database()

    existing = db.behaviors.find_one({"user_id": payload.user_id, "book_id": payload.book_id})
    if existing:
        # Aggregate behavior to better represent user interactions over time.
        db.behaviors.update_one(
            {"_id": existing["_id"]},
            {
                "$inc": {
                    "time_spent_minutes": payload.time_spent_minutes,
                    "pages_read": payload.pages_read,
                    "click_frequency": payload.click_frequency,
                    "liked_count": 1 if payload.liked else 0,
                    "saved_count": 1 if payload.saved else 0,
                }
            },
        )
        return {"message": "Behavior updated"}

    db.behaviors.insert_one(
        {
            "_id": str(uuid4()),
            **payload.model_dump(),
            "liked_count": 1 if payload.liked else 0,
            "saved_count": 1 if payload.saved else 0,
        }
    )
    return {"message": "Behavior tracked"}
