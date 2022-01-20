from fastapi import Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.repository import container
# from sqlalchemy.sql.functions import func
from .. import schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/containers",
    tags=['Containers']
)

@router.get("/", response_model=List[schemas.ContainerOut])
def get_continers(response: Response,db: Session = Depends(get_db)):
    return  container.get_containers(response, db)

@router.get("/search", response_model=List[schemas.ContainerOut])
def get_containers_search(db: Session = Depends(get_db), search: str=" "):
    return container.get_containers_search(db,search)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ContainerOut)
def create_container(post: schemas.ContainerCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return container.create_container(post, db, current_user)

@router.get("/{id}", response_model=schemas.ContainerOut)
def get_container(id: int, db: Session = Depends(get_db)):
    return container.get_container(id, db)

@router.delete("/{id}", response_model_exclude_none=True)
def delete_container(id: int, db: Session = Depends(get_db)):
    return container.delete_container(id, db) #Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.ContainerOut)
def update_container(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return container.update_container(id,updated_post,db)
