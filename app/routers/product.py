from fastapi import Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, oauth2
from ..database import get_db
from app.repository import product

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


@router.get("/", response_model=List[schemas.ProductOut])
def get_products(
    response: Response,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    return product.get_products(response, db)


@router.get("/", response_model=List[schemas.ProductOut])
def get_products(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    search: str = "",
):
    return product.get_products(db, search)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductOut
)
def create_product(
    post: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    return product.create_product(post, db)


@router.get("/{id}", response_model=schemas.ProductOut)
def get_product(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    return product.get_product(id, db)


@router.delete("/{id}", response_model_exclude_none=True)
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    return product.delete_product(id, db)


@router.put("/{id}", response_model=schemas.ProductOut)
def update_product(
    id: int,
    updated_post: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    return product.update_product(id, updated_post, db)
