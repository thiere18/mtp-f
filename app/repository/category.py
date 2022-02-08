from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

# from typing import

from sqlalchemy import func

# from sqlalchemy.sql.functions import func
from .. import models, schemas


router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])


def get_categories(response: Response, db: Session, current_user: int):
    categories = db.query(models.Category).filter(models.Category.deleted != True).all()
    response.headers["Content-Range"] = f"0-9/{len(categories)}"
    response.headers["X-Total-Count"] = "30"
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    return categories


def get_categories_search(db: Session, current_user: int, search: str):
    categories = (
        db.query(models.Category)
        .filter(models.Category.deleted != True, models.Category.name.contains(search))
        .all()
    )
    if not categories:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="No categories"
        )

    return categories


def create_categories(post: schemas.CategoryCreate, db: Session, current_user: int):

    new_category = models.Category(**post.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def get_category(id: int, db: Session, current_user: int):
    category = (
        db.query(models.Category)
        .filter(models.Category.id == id, models.Category.deleted != True)
        .first()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"category with id: {id} was not found",
        )
    return category


def delete_post(id: int, db: Session, current_user: int):
    post_query = db.query(models.Category).filter(
        models.Category.id == id, models.Category.deleted != True
    )
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    post.deleted = True
    db.commit()
    return post


def update_post(
    id: int, updated_post: schemas.CategoryCreate, db: Session, current_user: int
):
    post_query = db.query(models.Category).filter(
        models.Category.id == id, models.Category.deleted != True
    )
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
