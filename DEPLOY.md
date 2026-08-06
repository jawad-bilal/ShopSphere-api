# ShopSphere Backend — Deploy Guide (Vercel)

## Important: R2 is NOT a database

| Cloudflare product | What it is | Use for ShopSphere? |
|---|---|---|
| **R2** | Object storage (like S3) for files/images | Optional later for product images |
| **D1** | SQLite DB for Cloudflare Workers | Not a good fit with FastAPI on Vercel |
| **Neon / Supabase Postgres** | Real SQL database over the internet | **Use this for Vercel backend** |

For this FastAPI app on Vercel, create a **Postgres** database (Neon recommended, free tier).

---

## 1) Create Postgres (Neon — recommended)

1. Go to [https://neon.tech](https://neon.tech) and sign up
2. Create a project (e.g. `shopsphere`)
3. Copy the connection string (`DATABASE_URL`)  
   Example shape:  
   `postgresql://user:pass@ep-xxxx.region.aws.neon.tech/neondb?sslmode=require`

> You can also use Supabase → Project Settings → Database → Connection string (URI).

---

## 2) (Optional) Cloudflare R2 for files/images only

Only do this if you want to store uploaded images later. This does **not** replace `DATABASE_URL`.

1. Cloudflare dashboard → **R2 Object Storage**
2. Create bucket: `shopsphere-assets`
3. Manage R2 API Tokens → Create API token  
   - Permissions: Object Read & Write  
   - Apply to your bucket
4. Copy:
   - Account ID
   - Access Key ID
   - Secret Access Key
5. Optional: enable public access / custom domain for the bucket and set `R2_PUBLIC_BASE_URL`

Put those values in Vercel env vars from `.env.example` (`R2_*`).  
Current API does not upload to R2 yet; vars are reserved for later.

---

## 3) Create backend GitHub repo

From this folder only:

```bash
cd backend
git init
git add .
git commit -m "Initial ShopSphere API"
# create empty repo on GitHub, then:
git remote add origin https://github.com/YOUR_USER/shopsphere-backend.git
git branch -M main
git push -u origin main
```

---

## 4) Deploy on Vercel

1. [vercel.com](https://vercel.com) → Add New Project → import `shopsphere-backend`
2. Framework preset: **Other**
3. Root directory: `.` (repo root is already backend)
4. Add Environment Variables (from `.env.example`):

| Name | Example |
|---|---|
| `DATABASE_URL` | Neon/Supabase Postgres URL |
| `SECRET_KEY` | long random string |
| `CORS_ORIGINS` | `https://your-frontend.vercel.app` |
| `APP_NAME` | `ShopSphere API` |

5. Deploy
6. Test: `https://your-api.vercel.app/health` and `/docs`

---

## Local run

```bash
cp .env.example .env
# edit .env if needed
py -3.11 -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```
