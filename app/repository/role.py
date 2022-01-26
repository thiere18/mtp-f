from fastapi import Response, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db




def get_roles(response: Response,db: Session ):
    roles=db.query(models.Role).filter(models.Role.deleted!=True).all()
    response.headers["Content-Range"] = f"0-9/{len(roles)}"
    response.headers['X-Total-Count'] = '30' 
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    return roles

def create_role(post: schemas.RoleCreate, db: Session):
    new_role = models.Role(**post.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

def get_role(id: int, db: Session):
    role = db.query(models.Role).filter(models.Role.id == id,models.Role.deleted!=True).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"role with id: {id} was not found")
    return role

def delete_role(id: int, db: Session):
    role_query = db.query(models.Role).filter(models.Role.id == id,models.Role.deleted!=True)
    role = role_query.first()
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"role with id: {id} does not exist")
    role.deleted = True
    db.commit()
    return role # Response(status_code=status.HTTP_204_NO_CONTENT)


def update_role(id: int, updated_post: schemas.CategoryCreate, db: Session):
    role_query = db.query(models.Role).filter(models.Role.id == id,models.Role.deleted!=True)
    role = role_query.first()
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"role with id: {id} does not exist")  
    role_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return role_query.first()
