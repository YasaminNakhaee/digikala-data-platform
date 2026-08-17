#from fastapi import FastAPI, Depends
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func,desc
import pandas as pd 
import io 
from fastapi.responses import StreamingResponse
from src.db.database import engine
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

@app.get("/products/search", response_model=List[ProductResponse])
def search_products(q:str, db:Session=Depends(get_db)):
    products = db.query(Product).filter(Product.title.contains(q)).all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@app.get("/products/{product_id}/comments/top", response_model=List[CommentResponse])
def get_top_comments(product_id:int, db:Session=Depends(get_db)):
    top_comments = db.query(Comment).filter(Comment.product_id == product_id, Comment.rate >= 4).all()
    return top_comments

@app.get("/products/{product_id}/comments/count")
def get_comments_count(product_id:int, db:Session=Depends(get_db)):
    total_comments_count = db.query(Comment).filter(Comment.product_id == product_id).count()
    return {
        "product_id":product_id,
        "total_comments_count":total_comments_count
    }


@app.get("/analytics/top-products")
def get_top_products(db: Session=Depends(get_db)):
    results = db.query(
        Comment.product_id ,
        func.count(Comment.id).label("total_comments"),
        func.avg(Comment.rate).label("average_rate")
    ).group_by(Comment.product_id).order_by(desc("total_comments")).limit(5).all()

    report = []

    for row in results :
        report.append({
            "product_id": row.product_id,
            "total_comments": row.total_comments,
            "average_rate": round(row.average_rate,2) if row.average_rate else None
        })

    return report

@app.get("/analytics/export_report")
def export_analytics_csv(db: Session=Depends(get_db)):
    query = db.query(Comment.product_id, Comment.rate).statement
    df = pd.read_sql(query, engine)

    report_df = df.groupby("product_id").agg(
        total_comments = ("product_id","count"),
        average_rate = ("rate","mean")
    ).reset_index()

    stream = io.StringIO()
    report_df.to_csv(stream, index = False)#

    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename = digikala_analytics_report.csv"
    return response
