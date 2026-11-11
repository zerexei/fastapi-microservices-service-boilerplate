# FastAPI Microservice Template

> A FastAPI microservice template using SQLModel, PostgreSQL, and Redis, managed with `uv`.

---

## Tech Stack

* **Framework:** FastAPI
* **Database:** SQLModel + PostgreSQL (`asyncpg`)
* **Cache:** `redis-py` (async client)
* **Configuration:** Pydantic Settings
* **Package Manager:** `uv`
* **Testing:** Pytest + HTTPX

---

## Project Structure

```text
├── app/
│   ├── core/
│   │   ├── cache.py       # Async Redis client
│   │   └── database.py    # Async SQLAlchemy engine & session factory
│   ├── main.py            # Application entrypoint & lifespan events
│   ├── models.py          # SQLModel database tables
│   ├── schemas.py         # Pydantic DTOs
│   ├── router.py          # API endpoints
│   └── services.py        # Business logic layer
├── tests/
│   ├── conftest.py        # Pytest fixtures & SQLite setup
│   └── test_users.py      # Endpoint tests
├── pyproject.toml
├── Dockerfile
└── .gitignore
```

---

## Local Setup

### 1. Install Dependencies

```bash
uv sync --locked
```

### 2. Environment Variables

Create a `.env` file:

```env
APP_NAME="FastAPI Microservice"
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/app_db"
REDIS_URL="redis://localhost:6379/0"
```

### 3. Run Development Server

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Testing

```bash
uv run pytest -v
```

---

## Docker

Build the container image:

```bash
docker build -t fastapi-microservice .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env fastapi-microservice
```