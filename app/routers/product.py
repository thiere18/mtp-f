from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from enum import Enum
from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

from enum import Enum
router = APIRouter(
    prefix="/api/v1/products",
    tags=['Products']
)





@router.get("/", response_model=List[schemas.ProductOut])
def get_products(response: Response,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    products =db.query(models.Product).filter(models.Product.deleted!=True).all()

    response.headers["Content-Range"] = f"0-9/{len(products)}"
    response.headers['X-Total-Count'] = '30' 
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'

    return products

@router.get("/", response_model=List[schemas.ProductOut])
def get_products(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),  search: str= ""):

    return (
        db.query(models.Product)
        .filter(
            models.Product.deleted != True,
            models.Product.designation.contains(search),
        )
        .all()
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductOut)
def create_product(post: schemas.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    new_product = models.Product(quantity_left=post.quantity_init,prix_revient=post.prix_achat+post.frais,**post.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/{id}", response_model=schemas.ProductOut)
def get_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  

    product = db.query(models.Product).filter(models.Product.id == id,models.Product.deleted!=True).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} was not found")

    return product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    product_query = db.query(models.Product).filter(models.Product.id == id,models.Product.deleted!=True)

    product = product_query.first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} does not exist")
    product.deleted = True
    db.commit()
    return product


@router.put("/{id}", response_model=schemas.ProductOut)
def update_product(id: int, updated_post: schemas.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):



    product_query = db.query(models.Product).filter(models.Product.id == id,models.Product.deleted!=True)

    product = product_query.first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} does not exist")


    product_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return product_query.first()
