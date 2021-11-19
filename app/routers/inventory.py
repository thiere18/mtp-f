from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/inventories",
    tags=['Inventory']
)

# get product of each container

@router.get("/container/{id}", response_model=List[schemas.ProductOut])
def get_container_prod(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  
# verify if the container exist
    existence= db.query(models.Category).filter(models.Category.id==id,models.Category.deleted!=True).first()
    if existence==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"container with id: {id} was not found")
         
    products = db.query(models.Product).filter(models.Product.container_id == id,models.Category.deleted!=True).all()

    if not products:
         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f"this container has no products for now")

    return products

# get product of each category

@router.get("/category/{id}", response_model=List[schemas.ProductOut])
def get_category_prod(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  
# verify if the container exist
    existence= db.query(models.Category).filter(models.Category.id==id,models.Category.deleted!=True).first()
    if existence==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"category with id: {id} was not found")
         
    products = db.query(models.Product).filter(models.Product.category_id == id,models.Category.deleted!=True).all()

    if not products:
         raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"this category has no products for now")
    return products



