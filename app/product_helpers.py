from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import Product, Review
from .schemas import ProductOut


def product_to_out(db: Session, product: Product) -> ProductOut:
    average, count = (
        db.query(func.avg(Review.rating), func.count(Review.id))
        .filter(Review.product_id == product.id)
        .one()
    )
    return ProductOut(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        image=product.image,
        category=product.category,
        stock=product.stock,
        average_rating=round(float(average or 0), 1),
        review_count=int(count or 0),
    )
