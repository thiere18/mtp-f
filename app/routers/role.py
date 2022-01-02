from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/roles",
    tags=['Roles']
)


@router.get("/", response_model=List[schemas.RoleOut])
def get_roles(response: Response,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), ):
    roles=db.query(models.Role).filter(models.Role.deleted!=True).all()
    response.headers["Content-Range"] = f"0-9/{len(roles)}"
    response.headers['X-Total-Count'] = '30' 
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'

    return roles

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RoleOut)
def create_role(post: schemas.RoleCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    new_role = models.Role(**post.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role


@router.get("/{id}", response_model=schemas.RoleOut)
def get_role(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  

    role = db.query(models.Role).filter(models.Role.id == id,models.Role.deleted!=True).first()

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"role with id: {id} was not found")

    return role

@router.delete("/{id}", response_model_exclude_none=True)
def delete_role(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    role_query = db.query(models.Role).filter(models.Role.id == id,models.Role.deleted!=True)

    role = role_query.first()

    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"role with id: {id} does not exist")
    role.deleted = True
    db.commit()
    return role # Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.RoleOut)
def update_role(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):



    role_query = db.query(models.Role).filter(models.Role.id == id,models.Role.deleted!=True)

    role = role_query.first()

    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"role with id: {id} does not exist")

    
    role_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return role_query.first()
