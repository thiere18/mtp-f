from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/depense",
    tags=['Depense']
)


@router.get("/", response_model=List[schemas.DepenseOut])
def get_depenses(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,):

    depenses=db.query(models.Depense).filter(models.Depense.deleted!=True).all()
    return  depenses

@router.get("/search", response_model=List[schemas.DepenseOut])
def get_depenses(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: str = ""):

    depenses=db.query(models.Depense).filter(models.Depense.deleted!=True,models.Depense.motif.contains(search)).all()
    return  depenses


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DepenseOut)
def create_depense(post: schemas.Depensecreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    new_depense = models.Depense(**post.dict())
    db.add(new_depense)
    db.commit()
    db.refresh(new_depense)

    return new_depense


@router.get("/{id}", response_model=schemas.DepenseOut)
def get_depense(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  

    depense = db.query(models.Depense).filter(models.Depense.id == id,models.Depense.deleted!=True).first()

    if not depense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"depense with id: {id} was not found")

    return depense


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_depot(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    depense_query = db.query(models.Depense).filter(models.Depense.id == id,models.Depense.deleted!=True)

    depense = depense_query.first()

    if depense == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"depense with id: {id} does not exist")
    depense.deleted = True
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.DepotOut)
def update_depot(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):



    depense_query = db.query(models.Depense).filter(models.Depense.id == id,models.Depense.deleted!=True)

    depense = depense_query.first()

    if depense == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"depense with id: {id} does not exist")

    
    depense_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return depense_query.first()
