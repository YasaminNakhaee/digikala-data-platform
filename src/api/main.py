from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from src.db.database import get_db
from src.db.models import Product,Comment
from src.api.schemas import ProductResponse,CommentResponse

app = FastAPI(
    title="digikala data platform api Yasamin and Davood",
    description="سیستم مدیریت داده های دیجی کالا شعبه یاسمین و داوود",
    version="1.0.0"
)

@app.get("/products",response_model=List[ProductResponse])
def get_all_products(skip:int=0, limit:int=10, db:Session=Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{products_id}/comments",response_model=List[CommentResponse])
def get_product_comments(product_id:int,db:Session=Depends(get_db)):
    comments = db.query(Comment).filter(Comment.product_id == product_id).all()
    return comments
