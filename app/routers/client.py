from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/clients",
    tags=['Clients']
)


@router.get("/", response_model=List[schemas.ClientOut])
def get_clientss(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0):

    clients=db.query(models.Client).filter(models.Client.deleted!=True).all()
    return  clients

@router.get("/search", response_model=List[schemas.ClientOut])
def search_client(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: str = ""):

    clients=db.query(models.Client).filter(models.Client.deleted!=True,models.Client.name.contains(search)).all()
    return  clients

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ClientOut)
def create_client(post: schemas.DepotCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    new_client = models.Client(**post.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client


@router.get("/{id}", response_model=schemas.ClientOut)
def get_client(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  

    client = db.query(models.Client).filter(models.Client.id == id,models.Client.deleted!=True).first()

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"client with id: {id} was not found")

    return client


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_depot(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    client_query = db.query(models.Client).filter(models.Client.id == id,models.Client.deleted!=True)

    client = client_query.first()

    if client == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"client with id: {id} does not exist")
    client.deleted = True
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.ClientOut)
def update_depot(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):



    client_query = db.query(models.Client).filter(models.Client.id == id,models.Client.deleted!=True)

    client = client_query.first()

    if client == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"client with id: {id} does not exist")

    
    client_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return client_query.first()
