from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/containers",
    tags=['Containers']
)


@router.get("/", response_model=List[schemas.ContainerOut])
def get_categories(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    containers=db.query(models.Container).filter(models.Container.deleted!=True).all()
    return  containers


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ContainerOut)
def create_container(post: schemas.ContainerCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    new_container = models.Container(**post.dict())
    db.add(new_container)
    db.commit()
    db.refresh(new_container)

    return new_container


@router.get("/{id}", response_model=schemas.ContainerOut)
def get_container(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  

    container = db.query(models.Container).filter(models.Container.id == id,models.Container.deleted!=True).first()

    if not container:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"container with id: {id} was not found")

    return container


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_container(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    container_query = db.query(models.Container).filter(models.Container.id == id,models.Container.deleted!=True)

    container = container_query.first()

    if container == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"container with id: {id} does not exist")
    container.deleted = True
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.ContainerOut)
def update_container(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):



    container_query = db.query(models.Container).filter(models.Container.id == id,models.Container.deleted!=True)

    container = container_query.first()

    if container == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"container with id: {id} does not exist")

    
    container_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return container_query.first()
