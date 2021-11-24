from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/dettes",
    tags=['Dettes']
)


@router.get("/", response_model=List[schemas.DetteOut])
def get_dettes(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0):

    dettes=db.query(models.Dette).filter(models.Dette.deleted!=True).all()
    return  dettes

@router.get("/search", response_model=List[schemas.DetteOut])
def search_dette_by_reference(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: str = ""):

    dettes=db.query(models.Dette).filter(models.Dette.deleted!=True,models.Dette.reference.contains(search)).all()
    return  dettes

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DetteOut)
def create_dette(post: schemas.DetteCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    new_dette = models.Dette(**post.dict())
    db.add(new_dette)
    db.commit()
    db.refresh(new_dette)

    return new_dette


@router.get("/{id}", response_model=schemas.DetteOut)
def get_dette(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  

    dette = db.query(models.Dette).filter(models.Dette.id == id,models.Dette.deleted!=True).first()

    if not dette:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"dette with id: {id} was not found")

    return dette


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dette(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    dette_query = db.query(models.Dette).filter(models.Dette.id == id,models.Dette.deleted!=True)

    dette = dette_query.first()

    if dette == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"dette with id: {id} does not exist")
    dette.deleted = True
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.DetteOut)
def update_dette(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):



    dette_query = db.query(models.Dette).filter(models.Dette.id == id,models.Dette.deleted!=True)

    dette = dette_query.first()

    if dette == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"dette with id: {id} does not exist")

    
    dette_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return dette_query.first()
