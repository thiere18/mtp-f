from fastapi import Depends
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from . import database,schemas,models
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hashpass(password:str):
    return pwd_context.hash(password)


def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(
        name=role.name,
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def create_user( db: Session, user: schemas.UserCreate ):

    # hash the password - user.password
    # user.password = hashed_password

    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hash(user.password),
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_role(role_id:int, db: Session = Depends(database.get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="role not found")
    return role.name

    
