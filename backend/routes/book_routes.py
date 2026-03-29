"""Routes for book CRUD/search."""
from uuid import uuid4
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from auth import get_current_user
from database import get_database
from models.schemas import BookCreate, BookOut


router = APIRouter(tags=["books"])


@router.post("/books", response_model=BookOut)
def create_book(payload: BookCreate, _: dict = Depends(get_current_user)):
    db = get_database()

    book_id = str(uuid4())
    doc = {
        "_id": book_id,
        "title": payload.title,
        "author": payload.author,
        "genre": payload.genre,
        "description": payload.description,
    }
    db.books.insert_one(doc)
    return BookOut(id=book_id, **payload.model_dump())


@router.get("/books", response_model=List[BookOut])
def get_books(search: Optional[str] = Query(default=None)):
    db = get_database()

    query = {}
    if search:
        query = {
            "$or": [
                {"title": {"$regex": search, "$options": "i"}},
                {"author": {"$regex": search, "$options": "i"}},
                {"genre": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
            ]
        }

    books = list(db.books.find(query))
    return [BookOut(id=b["_id"], title=b["title"], author=b["author"], genre=b["genre"], description=b["description"]) for b in books]
