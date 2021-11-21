from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/depots",
    tags=['Depots']
)


@router.get("/", response_model=List[schemas.DepotOut])
def get_depots(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    depots=db.query(models.Depot).filter(models.Depot.deleted!=True).all()
    return  depots


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DepotOut)
def create_depot(post: schemas.DepotCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    new_depot = models.Depot(**post.dict())
    db.add(new_depot)
    db.commit()
    db.refresh(new_depot)

    return new_depot


@router.get("/{id}", response_model=schemas.DepotOut)
def get_depot(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  

    depot = db.query(models.Depot).filter(models.Depot.id == id,models.Depot.deleted!=True).first()

    if not depot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"depot with id: {id} was not found")

    return depot


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_depot(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    depot_query = db.query(models.Depot).filter(models.Depot.id == id,models.Depot.deleted!=True)

    depot = depot_query.first()

    if depot == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"depot with id: {id} does not exist")
    depot.deleted = True
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.DepotOut)
def update_depot(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):



    depot_query = db.query(models.Depot).filter(models.Depot.id == id,models.Depot.deleted!=True)

    depot = depot_query.first()

    if depot == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"depot with id: {id} does not exist")

    
    depot_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return depot_query.first()
