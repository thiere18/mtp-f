from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.utils import get_user_role
from .. import database, models, utils, oauth2

def login(db: Session ,user_credentials: OAuth2PasswordRequestForm , ):

    user = db.query(models.User).filter((models.User.email == user_credentials.username) | (models.User.username == user_credentials.username)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials'
        )
#
    permissions=get_user_role(user.role_id,db)
    access_token = oauth2.create_access_token(data={"user_id": user.id,"permissions":permissions})

    return {"access_token": access_token, "token_type": "bearer", "permission":permissions}
