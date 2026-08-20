from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def _column_names(inspector, table: str) -> set[str]:
    return {column["name"] for column in inspector.get_columns(table)}


def _add_column(engine: Engine, statement: str) -> None:
    with engine.begin() as connection:
        connection.execute(text(statement))


def ensure_schema(engine: Engine) -> None:
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    is_sqlite = engine.dialect.name == "sqlite"

    if "users" in tables:
        user_columns = _column_names(inspector, "users")
        if "role" not in user_columns:
            _add_column(
                engine,
                "ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'customer'",
            )
        if "credentials_revoked_at" not in user_columns:
            _add_column(
                engine,
                "ALTER TABLE users ADD COLUMN credentials_revoked_at TIMESTAMP",
            )

    if "products" in tables:
        product_columns = _column_names(inspector, "products")
        if "stock" not in product_columns:
            _add_column(
                engine,
                "ALTER TABLE products ADD COLUMN stock INTEGER NOT NULL DEFAULT 25",
            )
        if "is_active" not in product_columns:
            default_active = "1" if is_sqlite else "TRUE"
            _add_column(
                engine,
                f"ALTER TABLE products ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT {default_active}",
            )
