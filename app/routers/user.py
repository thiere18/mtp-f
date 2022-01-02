from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils,oauth2
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/users",
    tags=['Users']
)

# /users/
# /users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.get('/{id}', response_model=schemas.UserInvoices)
def get_user(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user) ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user

@router.get('/', response_model=List[schemas.UserInvoices])
def get_user_all(response:Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).all()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User with id:  does not exist',
        )
    response.headers["Content-Range"] = f"0-9/{len(user)}"
    response.headers['X-Total-Count'] = '30' 
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'


    return user


@router.put('/edit')
def change_password( mode:schemas.UpdatePassword,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    if not utils.verify( mode.actual_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Password does not match',
        )

    hashed_pass = utils.hashpass(mode.new_password)
    user.password = hashed_pass
    db.commit()
    return {"msg":"Password changed successfully"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    product_query = db.query(models.Product).filter(models.Product.id == id,models.Product.deleted!=True)

    product = product_query.first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} does not exist")
    product.deleted = True
    db.commit()
    return product