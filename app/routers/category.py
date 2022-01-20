from fastapi import  Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.repository import category
# from sqlalchemy.sql.functions import func
from .. import  schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/categories",
    tags=['Categories']
)

@router.get("/", response_model=List[schemas.CategoryOut])
def get_categories(response:Response,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return  category.get_categories(response, db, current_user)

@router.get("/search", response_model=List[schemas.CategoryOut])
def get_categories(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: str = ""):
    return  category.get_categories_search(db, current_user, search)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryOut)
def create_categories(post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return category.create_categories()

@router.get("/{id}", response_model=schemas.CategoryOut)
def get_category(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return category.get_category(id, db, current_user)

@router.delete("/{id}",response_model_exclude_none=True)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return category.delete_post(id, db, current_user)

@router.put("/{id}", response_model=schemas.CategoryOut)
def update_post(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return category.update_post(id, updated_post, db, current_user)
