from fastapi import Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2

def get_magasins(response: Response,db: Session ):
    magasins=db.query(models.Magasin).filter(models.Magasin.deleted!=True).all()
    response.headers["Content-Range"] = f"0-9/{len(magasins)}"
    response.headers['X-Total-Count'] = '30' 
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    return magasins

def create_magasin(post: schemas.MagasinCreate, db: Session , current_user: int = Depends(oauth2.get_current_user)):
    new_magasin = models.Magasin(gerant_id=current_user.id, **post.dict())
    db.add(new_magasin)
    db.commit()
    db.refresh(new_magasin)
    return new_magasin

def get_magasin(id: int, db: Session ):
    magasin = db.query(models.Magasin).filter(models.Magasin.id == id,models.Magasin.deleted!=True).first()
    if not magasin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"magasin with id: {id} was not found")
    return magasin

def delete_magasin(id: int, db: Session ):
    magasin_query = db.query(models.Magasin).filter(models.Magasin.id == id,models.Magasin.deleted!=True)
    magasin = magasin_query.first()
    if magasin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"magasin with id: {id} does not exist")
    magasin.deleted = True
    db.commit()
    return magasin # Response(status_code=status.HTTP_204_NO_CONTENT)

def update_magasin(id: int, updated_post: schemas.CategoryCreate, db: Session ):
    magasin_query = db.query(models.Magasin).filter(models.Magasin.id == id,models.Magasin.deleted!=True)
    magasin = magasin_query.first()
    if magasin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"magasin with id: {id} does not exist")
    magasin_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return magasin_query.first()
