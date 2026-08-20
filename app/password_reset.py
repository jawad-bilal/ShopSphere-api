import hmac
import secrets
from datetime import datetime, timedelta
from hashlib import sha256

from sqlalchemy.orm import Session

from .config import get_settings
from .constants import PASSWORD_RESET_EXPIRE_MINUTES
from .models import PasswordResetToken, User


def hash_reset_token(raw_token: str) -> str:
    secret = get_settings().secret_key.encode("utf-8")
    return hmac.new(secret, raw_token.encode("utf-8"), sha256).hexdigest()


def create_password_reset_token(db: Session, user: User) -> str:
    unused = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
        )
        .all()
    )
    now = datetime.utcnow()
    for token in unused:
        token.used_at = now

    raw_token = secrets.token_urlsafe(32)
    db.add(
        PasswordResetToken(
            user_id=user.id,
            token_hash=hash_reset_token(raw_token),
            expires_at=now + timedelta(minutes=PASSWORD_RESET_EXPIRE_MINUTES),
        )
    )
    db.commit()
    return raw_token


def consume_password_reset_token(db: Session, raw_token: str) -> User | None:
    token = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.token_hash == hash_reset_token(raw_token))
        .first()
    )
    if not token or token.used_at is not None:
        return None
    if token.expires_at < datetime.utcnow():
        return None

    token.used_at = datetime.utcnow()
    db.flush()
    return token.user
