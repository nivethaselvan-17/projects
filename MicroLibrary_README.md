# MicroLibrary

MicroLibrary is a smart book recommendation system that combines user behavior signals with book content.

## Features
- JWT signup/login
- Book catalog + search
- Behavior tracking (`time_spent_minutes`, `pages_read`, `click_frequency`, `liked`, `saved`)
- Hybrid recommender:
  - Content-based filtering (TF-IDF + cosine similarity)
  - Collaborative filtering (user-item interaction similarity)
  - Weighted hybrid score
- Simple recommendation caching (60-second in-memory TTL)

## Project Structure
```
backend/
  main.py
  auth.py
  database.py
  data/sample_books.json
  models/schemas.py
  routes/
  ml/recommender.py
frontend/
  src/components/
  src/pages/
```

## Run Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Optional environment variables
```bash
export MONGODB_URI="mongodb://localhost:27017"
export MONGODB_DB="microlibrary"
export JWT_SECRET="your-strong-secret"
export JWT_EXP_MINUTES="120"
```

### Seed sample data
```bash
curl -X POST http://localhost:8000/seed-sample-books
```

## Run Frontend
```bash
cd frontend
npm install
npm run start
```

Optional API URL:
```bash
export VITE_API_BASE_URL="http://localhost:8000"
```

## Main API Endpoints
- `POST /signup`
- `POST /login`
- `GET /books?search=...`
- `POST /books` (JWT)
- `POST /track-behavior` (JWT)
- `GET /recommendations/{user_id}` (JWT)
