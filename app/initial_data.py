#!/usr/bin/env python3

from app.database import SessionLocal
from app.schemas import UserCreate,RoleCreate
from app.utils import create_user, create_role

db = SessionLocal()

def init() -> None:
    create_user(
        db,
        UserCreate(
            username='admin',
            email='admin@fan.com',
            password='password',
            role_id=1,
        ),
    )

def ino() -> None:
    create_role(
        db, 
        RoleCreate(
            name='admin'
        ),
    )
    
if __name__ == "__main__":
    print("Creating superuser admin@fan.com with admin as username")
    ino()
    init()
    print("Superuser created")
