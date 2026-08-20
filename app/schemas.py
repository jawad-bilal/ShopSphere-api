from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from .constants import ROLE_CUSTOMER


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str = ROLE_CUSTOMER
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class ChangePasswordIn(BaseModel):
    current_password: str = Field(min_length=1, max_length=100)
    new_password: str = Field(min_length=6, max_length=100)
    confirm_password: str = Field(min_length=6, max_length=100)


class ForgotPasswordIn(BaseModel):
    email: EmailStr


class ResetPasswordIn(BaseModel):
    token: str = Field(min_length=16, max_length=255)
    new_password: str = Field(min_length=6, max_length=100)
    confirm_password: str = Field(min_length=6, max_length=100)


class MessageOut(BaseModel):
    message: str


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str
    category: str
    stock: int
    average_rating: float = 0.0
    review_count: int = 0

    model_config = {"from_attributes": True}


class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=3, max_length=1000)


class ReviewAuthorOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class ReviewOut(BaseModel):
    id: int
    rating: int
    comment: str
    created_at: datetime
    updated_at: datetime
    user: ReviewAuthorOut

    model_config = {"from_attributes": True}


class ReviewSummaryOut(BaseModel):
    average_rating: float
    review_count: int


class ProductReviewsOut(BaseModel):
    summary: ReviewSummaryOut
    reviews: list[ReviewOut]
    user_review: ReviewOut | None = None


class WishlistToggle(BaseModel):
    product_id: int


class WishlistItemOut(BaseModel):
    id: int
    created_at: datetime
    product: ProductOut

    model_config = {"from_attributes": True}


class OrderItemIn(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int = Field(ge=1)
    image: str


class OrderCreate(BaseModel):
    items: list[OrderItemIn]
    shipping_name: str = Field(min_length=2)
    shipping_address: str = Field(min_length=5)
    shipping_city: str = Field(min_length=2)
    shipping_zip: str = Field(min_length=3)
    payment_method: str = "card"
    card_number: str | None = None


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    name: str
    price: float
    quantity: int
    image: str

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: int
    total: float
    status: str
    shipping_name: str
    shipping_address: str
    shipping_city: str
    shipping_zip: str
    payment_method: str
    created_at: datetime
    items: list[OrderItemOut]

    model_config = {"from_attributes": True}
