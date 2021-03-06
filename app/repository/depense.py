from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/api/v1/depenses", tags=["Depenses"])


def get_depenses(response: Response, db: Session):
    depenses = db.query(models.Depense).filter(models.Depense.deleted != True).all()
    response.headers["Content-Range"] = f"0-9/{len(depenses)}"
    response.headers["X-Total-Count"] = "30"
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    return depenses


def get_depenses(db: Session, search: str = ""):
    return (
        db.query(models.Depense)
        .filter(
            models.Depense.deleted != True,
            models.Depense.motif.contains(search),
        )
        .all()
    )


def create_depense(post: schemas.Depensecreate, db: Session):
    # update magasin montant

    new_depense = models.Depense(**post.dict())
    db.add(new_depense)
    db.commit()
    db.refresh(new_depense)

    return new_depense


def get_depense(id: int, db: Session):
    depense = (
        db.query(models.Depense)
        .filter(models.Depense.id == id, models.Depense.deleted != True)
        .first()
    )
    if not depense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"depense with id: {id} was not found",
        )
    return depense


def delete_depense(id: int, db: Session):
    depense_query = db.query(models.Depense).filter(
        models.Depense.id == id, models.Depense.deleted != True
    )
    depense = depense_query.first()
    if depense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"depense with id: {id} does not exist",
        )
    depense.deleted = True
    db.commit()
    return depense  # Response(status_code=status.HTTP_204_NO_CONTENT)


def update_depense(id: int, updated_post: schemas.CategoryCreate, db: Session):
    depense_query = db.query(models.Depense).filter(
        models.Depense.id == id, models.Depense.deleted != True
    )
    depense = depense_query.first()
    if depense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"depense with id: {id} does not exist",
        )
    depense_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return depense_query.first()
