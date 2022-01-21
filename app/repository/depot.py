from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List,Any

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/depots",
    tags=['Depots']
)


def get_depots(response: Response,db: Session ):
    depots=db.query(models.Depot).filter(models.Depot.deleted!=True).all()
    response.headers["Content-Range"] = f"0-9/{len(depots)}"
    response.headers['X-Total-Count'] = '30' 
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    return  depots

def get_depots(db: Session ,search: str = ""):
    return (
        db.query(models.Depot)
        .filter(
            models.Depot.deleted != True, models.Depot.name.contains(search)
        )
        .all()
    )

def create_depot(post: schemas.DepotCreate, db: Session ):
    new_depot = models.Depot(**post.dict())
    db.add(new_depot)
    db.commit()
    db.refresh(new_depot)
    return new_depot


def get_depot(id: int, db: Session ):
    depot = db.query(models.Depot).filter(models.Depot.id == id,models.Depot.deleted!=True).first()
    if not depot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"depot with id: {id} was not found")
    return depot

def delete_depot(id: int, db: Session ):
    depot_query = db.query(models.Depot).filter(models.Depot.id == id,models.Depot.deleted!=True)
    depot = depot_query.first()
    if depot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"depot with id: {id} does not exist")
    depot.deleted = True
    db.commit()
    return depot #Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.DepotOut)
def update_depot(id: int, updated_post: schemas.CategoryCreate, db: Session ):
    depot_query = db.query(models.Depot).filter(models.Depot.id == id,models.Depot.deleted!=True)
    depot = depot_query.first()
    if depot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"depot with id: {id} does not exist")
    depot_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return depot_query.first()
