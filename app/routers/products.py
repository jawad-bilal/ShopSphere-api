from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Product, Review
from ..product_helpers import product_to_out
from ..schemas import ProductOut

router = APIRouter(prefix="/products", tags=["products"])

SORT_OPTIONS = {
    "default": Product.id.asc(),
    "price_asc": Product.price.asc(),
    "price_desc": Product.price.desc(),
    "name_asc": Product.name.asc(),
}


@router.get("", response_model=list[ProductOut])
def list_products(
    search: str | None = Query(default=None),
    category: str | None = Query(default=None),
    sort: str = Query(default="default"),
    db: Session = Depends(get_db),
):
    query = db.query(Product)

    if category and category.lower() != "all":
        query = query.filter(Product.category.ilike(category))

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            (Product.name.ilike(term)) | (Product.description.ilike(term))
        )

    if sort == "rating_desc":
        avg_rating = (
            db.query(
                Review.product_id,
                func.coalesce(func.avg(Review.rating), 0).label("avg_rating"),
            )
            .group_by(Review.product_id)
            .subquery()
        )
        query = query.outerjoin(avg_rating, Product.id == avg_rating.c.product_id).order_by(
            avg_rating.c.avg_rating.desc(),
            Product.id.asc(),
        )
    else:
        query = query.order_by(SORT_OPTIONS.get(sort, Product.id.asc()))

    products = query.all()
    return [product_to_out(db, product) for product in products]


@router.get("/categories", response_model=list[str])
def list_categories(db: Session = Depends(get_db)):
    rows = db.query(Product.category).distinct().order_by(Product.category.asc()).all()
    return [row[0] for row in rows]


@router.get("/{product_id}/related", response_model=list[ProductOut])
def related_products(
    product_id: int,
    limit: int = Query(default=4, ge=1, le=12),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    related = (
        db.query(Product)
        .filter(Product.category == product.category, Product.id != product_id)
        .order_by(Product.id.asc())
        .limit(limit)
        .all()
    )
    return [product_to_out(db, related_product) for related_product in related]


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_to_out(db, product)
