"""FastAPI entrypoint for MicroLibrary backend."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import get_database
from routes.auth_routes import router as auth_router
from routes.book_routes import router as book_router
from routes.behavior_routes import router as behavior_router
from routes.recommendation_routes import router as recommendation_router


app = FastAPI(title="MicroLibrary API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(book_router)
app.include_router(behavior_router)
app.include_router(recommendation_router)


@app.get("/")
def health():
    return {"status": "ok", "service": "MicroLibrary"}


@app.post("/seed-sample-books")
def seed_sample_books():
    """Insert sample books from JSON file when database is empty."""
    import json
    from pathlib import Path

    db = get_database()
    if db.books.count_documents({}) > 0:
        return {"message": "Books already exist"}

    data_path = Path(__file__).parent / "data" / "sample_books.json"
    with open(data_path, "r", encoding="utf-8") as file:
        books = json.load(file)

    db.books.insert_many(books)
    return {"message": f"Inserted {len(books)} books"}
