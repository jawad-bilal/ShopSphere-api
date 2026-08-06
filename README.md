# ShopSphere API

Python FastAPI backend for ShopSphere.

- Local: SQLite by default
- Production (Vercel): Postgres via `DATABASE_URL` (Neon/Supabase)

## Quick start

```bash
cp .env.example .env
py -3.11 -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

- Health: http://localhost:8000/health
- Docs: http://localhost:8000/docs

See [DEPLOY.md](./DEPLOY.md) for Vercel + database setup.
