from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/containers",
    tags=['Containers']
)

def get_containers(response: Response,db: Session ):
    containers=db.query(models.Container).filter(models.Container.deleted!=True).all()
    response.headers["Content-Range"] = f"0-9/{len(containers)}"
    response.headers['X-Total-Count'] = '30' 
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    return  containers

def get_containers_search(db: Session , search: str):

    return (
        db.query(models.Container)
        .filter(
            models.Container.deleted != True,
            models.Container.reference.contains(search),
        )
        .all()
    )

def create_container(post: schemas.ContainerCreate, db: Session, current_user: int ):
    new_container = models.Container(total=post.frais_dedouanement+post.charge_local+post.dechargement+post.frais_voyage+post.prix_transport+post.prix_achat+post.dechargement,**post.dict())
    db.add(new_container)
    db.commit()
    db.refresh(new_container)
    t=new_container.total
    #update capital to
    up=db.query(models.Magasin).filter(models.Magasin.gerant_id==current_user.id).first()
    if not up:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Problem")
    up.montant-=t
    db.commit()
    return new_container

def get_container(id: int, db: Session):
    container = db.query(models.Container).filter(models.Container.id == id,models.Container.deleted!=True).first()
    if not container:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"container with id: {id} was not found")
    return container

def delete_container(id: int, db: Session):
    container_query = db.query(models.Container).filter(models.Container.id == id,models.Container.deleted!=True)
    container = container_query.first()
    if container is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"container with id: {id} does not exist")
    container.deleted = True
    db.commit()
    return container #Response(status_code=status.HTTP_204_NO_CONTENT)

def update_container(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db)):
    container_query = db.query(models.Container).filter(models.Container.id == id,models.Container.deleted!=True)
    container = container_query.first()
    if container is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"container with id: {id} does not exist")
    container_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return container_query.first()
