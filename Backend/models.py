from sqlalchemy import Column, Integer, String, Boolean, Float, Date, Enum, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    reset_token = Column(String, nullable=True)
    reviews = relationship("Review", back_populates="user")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    stock_level = Column(Integer, nullable=False)
    reorder_threshold = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    image_url = Column(String, nullable=True)  # Store image file path or URL
    # created_at = Column(TIMESTAMP, server_default=func.now())
    # updated_at = Column(TIMESTAMP, onupdate=func.now())

     # Relationship: Each product belongs to a supplier
    supplier = relationship("Supplier", back_populates="products")

    # Relationship: A product can have multiple batches
    batches = relationship("Batch", back_populates="product")

    # Relationship: A product can have multiple reviews
    reviews = relationship("Review", back_populates="product")

class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_person = Column(String, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    # Relationship: A supplier can provide multiple products
    products = relationship("Product", back_populates="supplier")

class Batch(Base):
    __tablename__ = 'batches'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    quantity_received = Column(Integer, nullable=False)
    received_date = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=True)  # Nullable for non-expiring items
    batch_status = Column(Enum('Active', 'Expired', 'Sold Out', name='batch_status'), nullable=False, default='Active')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="batches")

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")