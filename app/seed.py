from sqlalchemy.orm import Session

from .models import Product

DEFAULT_STOCK = 25

SEED_PRODUCTS = [
    {
        "name": "Classic T-Shirt",
        "description": "High-quality cotton T-Shirt. Perfect for casual wear with a comfortable fit and durable fabric.",
        "price": 19.99,
        "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&h=600&fit=crop&crop=center",
        "category": "Clothing",
        "stock": 40,
    },
    {
        "name": "Denim Jeans",
        "description": "Comfortable blue jeans made from premium denim. Classic fit with modern styling.",
        "price": 49.99,
        "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=600&h=600&fit=crop&crop=center",
        "category": "Clothing",
        "stock": 28,
    },
    {
        "name": "Running Sneakers",
        "description": "Stylish running sneakers with excellent cushioning and support for all-day comfort.",
        "price": 89.99,
        "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&h=600&fit=crop&crop=center",
        "category": "Footwear",
        "stock": 18,
    },
    {
        "name": "Wireless Headphones",
        "description": "Premium wireless headphones with noise cancellation and superior sound quality.",
        "price": 129.99,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&h=600&fit=crop&crop=center",
        "category": "Electronics",
        "stock": 12,
    },
    {
        "name": "Leather Wallet",
        "description": "Genuine leather wallet with multiple card slots and a sleek design.",
        "price": 34.99,
        "image": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=600&h=600&fit=crop&crop=center",
        "category": "Accessories",
        "stock": 35,
    },
    {
        "name": "Smartwatch",
        "description": "Feature-rich smartwatch with fitness tracking, notifications, and long battery life.",
        "price": 199.99,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&h=600&fit=crop&crop=center",
        "category": "Electronics",
        "stock": 8,
    },
    {
        "name": "Backpack",
        "description": "Durable and spacious backpack perfect for work, travel, or outdoor adventures.",
        "price": 59.99,
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&h=600&fit=crop&crop=center",
        "category": "Accessories",
        "stock": 22,
    },
    {
        "name": "Sunglasses",
        "description": "Stylish sunglasses with UV protection and a timeless design.",
        "price": 24.99,
        "image": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=600&h=600&fit=crop&crop=center",
        "category": "Accessories",
        "stock": 30,
    },
    {
        "name": "Hoodie",
        "description": "Soft fleece hoodie with a modern cut. Ideal for cool evenings and casual days.",
        "price": 44.99,
        "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=600&h=600&fit=crop&crop=center",
        "category": "Clothing",
        "stock": 15,
    },
    {
        "name": "Bluetooth Speaker",
        "description": "Portable speaker with rich bass and waterproof design for indoor and outdoor use.",
        "price": 79.99,
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600&h=600&fit=crop&crop=center",
        "category": "Electronics",
        "stock": 20,
    },
    {
        "name": "Canvas Sneakers",
        "description": "Lightweight everyday sneakers with breathable canvas and durable soles.",
        "price": 54.99,
        "image": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=600&h=600&fit=crop&crop=center",
        "category": "Footwear",
        "stock": 3,
    },
    {
        "name": "Minimal Desk Lamp",
        "description": "Warm LED desk lamp with adjustable brightness for focused work sessions.",
        "price": 39.99,
        "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&h=600&fit=crop&crop=center",
        "category": "Home",
        "stock": 0,
    },
]


def seed_products(db: Session) -> None:
    if db.query(Product).count() == 0:
        for item in SEED_PRODUCTS:
            db.add(Product(**item))
        db.commit()
        return

    for product in db.query(Product).all():
        if product.stock is None or product.stock < 0:
            product.stock = DEFAULT_STOCK
    db.commit()
