from fastapi import  Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from enum import Enum
router = APIRouter(
    prefix="/api/v1/products",
    tags=['Products']
)


def get_products(response: Response,db: Session, ):
    products =db.query(models.Product).filter(models.Product.deleted!=True).all()
    response.headers["Content-Range"] = f"0-9/{len(products)}"
    response.headers['X-Total-Count'] = '30' 
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    return products

def get_products(db: Session,   search: str= ""):
    return (
        db.query(models.Product)
        .filter(
            models.Product.deleted != True,
            models.Product.designation.contains(search),
        )
        .all()
    )


def create_product(post: schemas.ProductCreate, db: Session, ):
    new_product = models.Product(quantity_left=post.quantity_init,prix_revient=post.prix_achat+post.frais,**post.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_product(id: int, db: Session, ):
    product = db.query(models.Product).filter(models.Product.id == id,models.Product.deleted!=True).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} was not found")
    return product

def delete_product(id: int, db: Session, ):
    product_query = db.query(models.Product).filter(models.Product.id == id,models.Product.deleted!=True)
    product = product_query.first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} does not exist")
    product.deleted = True
    db.commit()
    return product


def update_product(id: int, updated_post: schemas.ProductCreate, db: Session, ):
    product_query = db.query(models.Product).filter(models.Product.id == id,models.Product.deleted!=True)
    product = product_query.first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} does not exist")
    product_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return product_query.first()
