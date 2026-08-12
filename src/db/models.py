from sqlalchemy import (
    Column , Integer, String, 
    Text, ForeignKey, Index
) 
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=True)
    category = Column(String(200), nullable=True)
    price = Column(Integer, nullable=True)

    comments = relationship("Comment", back_populates="product")

    __table_args__ = (
        Index("ix_product_title", "title"),
    )

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    title = Column(String(300), nullable=True)
    body = Column(Text, nullable=True)
    rate = Column(Integer, nullable=True)

    product = relationship("Product", back_populates="comments")

   