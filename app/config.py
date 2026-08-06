import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

# Load backend/.env for local development (no-op on Vercel where env vars are injected)
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def _split_origins(value: str) -> list[str]:
    return [origin.strip() for origin in value.split(",") if origin.strip()]


@lru_cache
def get_settings():
    return Settings()


class Settings:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "ShopSphere API")
        self.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me-in-production")
        self.access_token_expire_minutes = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", str(60 * 24 * 7))
        )
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")
        self.cors_origins = _split_origins(
            os.getenv(
                "CORS_ORIGINS",
                "http://localhost:5173,http://127.0.0.1:5173",
            )
        )
        # Optional: Cloudflare R2 object storage (NOT a database)
        self.r2_account_id = os.getenv("R2_ACCOUNT_ID", "")
        self.r2_access_key_id = os.getenv("R2_ACCESS_KEY_ID", "")
        self.r2_secret_access_key = os.getenv("R2_SECRET_ACCESS_KEY", "")
        self.r2_bucket_name = os.getenv("R2_BUCKET_NAME", "")
        self.r2_public_base_url = os.getenv("R2_PUBLIC_BASE_URL", "")
