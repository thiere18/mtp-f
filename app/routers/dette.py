from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.repository import dette

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/dettes",
    tags=['Dettes']
)

@router.get("/", response_model=List[schemas.DetteOut])
def get_dettes(response: Response,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return  dette.get_dettes(response,db)

@router.get("/search", response_model=List[schemas.DetteOut])
def search_dette_by_reference(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: str = ""):
    return dette.search_dette_by_reference(db, search)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DetteOut)
def create_dette(post: schemas.DetteCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return dette.create_dette(post, db)

@router.get("/{id}", response_model=schemas.DetteOut)
def get_dette(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return dette.get_dette(id, db)


@router.delete("/{id}", response_model_exclude_none=True)
def delete_dette(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return dette.delete_dette(id, db) # Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.DetteOut)
def update_dette(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return dette.update_dette(id, updated_post, db)
