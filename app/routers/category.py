from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/categories",
    tags=['Categories']
)


@router.get("/", response_model=List[schemas.CategoryOut])
def get_categories(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0):
    categories=db.query(models.Category).filter(models.Category.deleted!=True).all()  
    if not categories:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"No categories")
    return  categories

@router.get("/search", response_model=List[schemas.CategoryOut])
def get_categories(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: str = ""):
    categories=db.query(models.Category).filter(models.Category.deleted!=True,models.Category.name.contains(search)).all()  
    if not categories:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"No categories")
    return  categories

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryOut)
def create_categories(post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    new_category = models.Category(**post.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/{id}", response_model=schemas.CategoryOut)
def get_category(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  

    category = db.query(models.Category).filter(models.Category.id == id,models.Category.deleted!=True).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"category with id: {id} was not found")

    return category


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Category).filter(models.Category.id == id,models.Category.deleted!=True)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post.deleted = True
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.CategoryOut)
def update_post(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):



    post_query = db.query(models.Category).filter(models.Category.id == id,models.Category.deleted!=True)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
