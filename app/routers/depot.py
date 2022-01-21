from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.repository import depot
from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/depots",
    tags=['Depots']
)


@router.get("/", response_model=List[schemas.DepotOut])
def get_depots(response: Response,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return  depot.get_depots(response, db)

@router.get("/search", response_model=List[schemas.DepotOut])
def get_depots(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: str = ""):
    return depot.get_depots(db, search)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DepotOut)
def create_depot(post: schemas.DepotCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return depot.create_depot(post, db)

@router.get("/{id}", response_model=schemas.DepotOut)
def get_depot(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return depot.get_depot(id, db)

@router.delete("/{id}",response_model_exclude_none=True)
def delete_depot(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return depot.delete_depot(id, db)

@router.put("/{id}", response_model=schemas.DepotOut)
def update_depot(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return depot.update_depot(id,updated_post, db)
