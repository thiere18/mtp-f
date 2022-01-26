from typing import List
from fastapi import Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, oauth2
from ..database import get_db
from app.repository import user
router = APIRouter(
    prefix="/api/v1/users",
    tags=['Users']
)

# /users/
# /users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(post: schemas.UserCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return user.current_user(post, db)


@router.get('/{id}', response_model=schemas.UserInvoices)
def get_user(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user) ):
    return user.get_user(id, db)


@router.get('/', response_model=List[schemas.UserInvoices])
def get_user_all(response:Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return user.get_user_all(response, db)


@router.put('/edit')
def change_password( mode:schemas.UpdatePassword,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return user.change_password(mode,db, current_user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return user.delete_product(id, db)