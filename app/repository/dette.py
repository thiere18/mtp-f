from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/dettes",
    tags=['Dettes']
)


def get_dettes(response: Response,db: Session ):
    dettes=db.query(models.Dette).filter(models.Dette.deleted!=True).all()
    response.headers["Content-Range"] = f"0-9/{len(dettes)}"
    response.headers['X-Total-Count'] = '30' 
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    return  dettes

@router.get("/search", response_model=List[schemas.DetteOut])
def search_dette_by_reference(db: Session , search: str ):
    return (
        db.query(models.Dette)
        .filter(
            models.Dette.deleted != True,
            models.Dette.reference.contains(search),
        )
        .all()
    )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DetteOut)
def create_dette(post: schemas.DetteCreate, db: Session):
 
    new_dette = models.Dette(**post.dict())
    db.add(new_dette)
    db.commit()
    db.refresh(new_dette)
    return new_dette


def get_dette(id: int, db: Session):
    dette = db.query(models.Dette).filter(models.Dette.id == id,models.Dette.deleted!=True).first()
    if not dette:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"dette with id: {id} was not found")
    return dette

def delete_dette(id: int, db: Session):
    dette_query = db.query(models.Dette).filter(models.Dette.id == id,models.Dette.deleted!=True)
    dette = dette_query.first()
    if dette is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"dette with id: {id} does not exist")
    dette.deleted = True
    db.commit()
    return dette 

def update_dette(id: int, updated_post: schemas.CategoryCreate, db: Session , ):
    dette_query = db.query(models.Dette).filter(models.Dette.id == id,models.Dette.deleted!=True)
    dette = dette_query.first()
    if dette is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"dette with id: {id} does not exist")
    dette_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return dette_query.first()
