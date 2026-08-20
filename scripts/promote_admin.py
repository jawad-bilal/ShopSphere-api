import argparse
import sys

from app.constants import ROLE_ADMIN, ROLE_CUSTOMER, VALID_ROLES
from app.database import Base, SessionLocal, engine
from app.models import User
from app.schema_migrations import ensure_schema


def promote(email: str, role: str = ROLE_ADMIN) -> None:
    if role not in VALID_ROLES:
        raise SystemExit(f"Invalid role: {role}")

    ensure_schema(engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email.lower()).first()
        if not user:
            raise SystemExit(
                f"No user found for {email}. Sign up first, then run this script."
            )
        previous = user.role or ROLE_CUSTOMER
        user.role = role
        db.commit()
        print(f"Updated {user.email}: {previous} -> {user.role}")
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Promote a ShopSphere user to admin.")
    parser.add_argument(
        "email",
        help="Account email to promote, e.g. your-email@example.com",
    )
    parser.add_argument(
        "--role",
        default=ROLE_ADMIN,
        choices=sorted(VALID_ROLES),
        help="Role to assign (default: admin)",
    )
    args = parser.parse_args()
    promote(args.email, args.role)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
