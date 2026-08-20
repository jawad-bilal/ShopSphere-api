from sqlalchemy.orm import Session

from .models import Product


def active_products_query(db: Session):
    return db.query(Product).filter(Product.is_active.is_(True))


def get_active_product(db: Session, product_id: int) -> Product | None:
    return active_products_query(db).filter(Product.id == product_id).first()
