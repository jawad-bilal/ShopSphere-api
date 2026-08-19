from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from ..auth import get_current_user, get_optional_user
from ..database import get_db
from ..models import Product, Review, User
from ..schemas import ProductReviewsOut, ReviewCreate, ReviewOut, ReviewSummaryOut

router = APIRouter(prefix="/products", tags=["reviews"])


def _build_summary(db: Session, product_id: int) -> ReviewSummaryOut:
    average, count = (
        db.query(func.avg(Review.rating), func.count(Review.id))
        .filter(Review.product_id == product_id)
        .one()
    )
    return ReviewSummaryOut(
        average_rating=round(float(average or 0), 1),
        review_count=int(count or 0),
    )


def _serialize_review(review: Review) -> ReviewOut:
    return ReviewOut.model_validate(review)


@router.get("/{product_id}/reviews", response_model=ProductReviewsOut)
def list_product_reviews(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    reviews = (
        db.query(Review)
        .options(joinedload(Review.user))
        .filter(Review.product_id == product_id)
        .order_by(Review.created_at.desc())
        .all()
    )

    user_review = None
    if current_user:
        own = next((review for review in reviews if review.user_id == current_user.id), None)
        if own:
            user_review = _serialize_review(own)

    return ProductReviewsOut(
        summary=_build_summary(db, product_id),
        reviews=[_serialize_review(review) for review in reviews],
        user_review=user_review,
    )


@router.post("/{product_id}/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def upsert_review(
    product_id: int,
    payload: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = (
        db.query(Review)
        .filter(
            Review.product_id == product_id,
            Review.user_id == current_user.id,
        )
        .first()
    )

    if existing:
        existing.rating = payload.rating
        existing.comment = payload.comment.strip()
        db.commit()
        db.refresh(existing)
        review = (
            db.query(Review)
            .options(joinedload(Review.user))
            .filter(Review.id == existing.id)
            .first()
        )
        return _serialize_review(review)

    review = Review(
        user_id=current_user.id,
        product_id=product_id,
        rating=payload.rating,
        comment=payload.comment.strip(),
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    review = (
        db.query(Review)
        .options(joinedload(Review.user))
        .filter(Review.id == review.id)
        .first()
    )
    return _serialize_review(review)


@router.delete("/{product_id}/reviews", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    review = (
        db.query(Review)
        .filter(
            Review.product_id == product_id,
            Review.user_id == current_user.id,
        )
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()
