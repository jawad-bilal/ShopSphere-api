from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {"from_attributes": True}


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str
    category: str

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
