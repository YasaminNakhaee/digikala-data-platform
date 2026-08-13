from pydantic import BaseModel
from typing import Optional

class ProductResponse(BaseModel):
    id : int
    title : Optional[str] = None
    category : Optional[str] = None
    price : Optional[int] = None

    class Config:
        from_attributes = True

class CommentResponse(BaseModel):
    id : int
    title : Optional[str] = None
    body : Optional[str] = None
    rate : Optional[int] = None

    class Config:
        from_attributes = True