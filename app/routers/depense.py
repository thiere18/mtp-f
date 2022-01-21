from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.repository import depense
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/depenses",
    tags=['Depenses']
)


@router.get("/", response_model=List[schemas.DepenseOut],response_model_exclude_none=True)
def get_depenses(response: Response,db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    return depense.get_depenses(response,db)

@router.get("/search", response_model=List[schemas.DepenseOut])
def get_depenses(db: Session = Depends(get_db), search: str = "",  current_user: int = Depends(oauth2.get_current_user)):
    return depense.get_depenses(db, search)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DepenseOut)
def create_depense(post: schemas.Depensecreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return depense.create_depense(post, db)


@router.get("/{id}", response_model=schemas.DepenseOut)
def get_depense(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return depense.get_depense(id,db)

@router.delete("/{id}", response_model_exclude_none=True)
def delete_depense(id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    return depense.delete_depense(id, db)
#Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.DepotOut)
def update_depense(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    return depense.update_depense(id,updated_post, db)
