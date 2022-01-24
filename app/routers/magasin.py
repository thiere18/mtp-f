from fastapi import  Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.repository import magasin
from .. import schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/magasins",
    tags=['Magasins']
)

@router.get("/", response_model=List[schemas.MagasinOut])
def get_magasins(response: Response,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), ):
    return magasin.get_magasins(response,db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MagasinOut)
def create_magasin(post: schemas.MagasinCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return magasin.create_magasin(post,db,current_user)

@router.get("/{id}", response_model=schemas.MagasinOut)
def get_magasin(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return magasin.get_magasin(id, db)

@router.delete("/{id}", response_model_exclude_none=True)
def delete_magasin(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return magasin.delete_magasin(id, db)

@router.put("/{id}", response_model=schemas.MagasinOut)
def update_magasin(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return magasin.update_magasin(id, updated_post, db)
