from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/magasins",
    tags=['Magasins']
)


@router.get("/", response_model=List[schemas.MagasinOut])
def get_magasins(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    magasin=db.query(models.Magasin).filter(models.Magasin.deleted!=True).all()
    return  magasin


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MagasinOut)
def create_magasin(post: schemas.MagasinCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    new_magasin = models.Magasin(**post.dict())
    db.add(new_magasin)
    db.commit()
    db.refresh(new_magasin)

    return new_magasin


@router.get("/{id}", response_model=schemas.MagasinOut)
def get_magasin(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  

    magasin = db.query(models.Magasin).filter(models.Magasin.id == id,models.Magasin.deleted!=True).first()

    if not magasin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"magasin with id: {id} was not found")

    return magasin


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_magasin(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    magasin_query = db.query(models.Magasin).filter(models.Magasin.id == id,models.Magasin.deleted!=True)

    magasin = magasin_query.first()

    if magasin == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"magasin with id: {id} does not exist")
    magasin.deleted = True
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.MagasinOut)
def update_magasin(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):



    magasin_query = db.query(models.Magasin).filter(models.Magasin.id == id,models.Magasin.deleted!=True)

    magasin = magasin_query.first()

    if magasin == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"magasin with id: {id} does not exist")

    
    magasin_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return magasin_query.first()
