from fastapi import  Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.repository import client
# from sqlalchemy.sql.functions import func
from .. import  schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/clients",
    tags=['Clients']
)

@router.get("/", response_model=List[schemas.ClientOut])
def get_clientss(response: Response,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return  client.get_clientss(response,db)

@router.get("/search", response_model=List[schemas.ClientOut])
def search_client(db: Session = Depends(get_db), search: str = "", current_user: int = Depends(oauth2.get_current_user)):
    return client.search_client(db, search)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ClientOut)
def create_client(post: schemas.ClientCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return client.create_client(post, db)

@router.get("/{id}", response_model=schemas.ClientOuts)
def get_client(id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    return client.get_client(id, db)

@router.delete("/{id}",response_model_exclude_none=True)
def delete_client(id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    return client.delete_client(id,db) #Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.ClientOut)
def update_client(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return client.update_depot(id, updated_post, db)
