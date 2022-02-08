from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func

# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/api/v1/inventories", tags=["Inventory"])

# get product of each container

# paid invoice
@router.get("/paid", response_model=List[schemas.InvoiceOut])
def get_paid_invoice(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    invoice = (
        db.query(models.Invoice)
        .filter(models.Invoice.deleted != True, models.Invoice.paid != False)
        .all()
    )

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no paid invoice found",
        )

    return invoice


# unpaid invoice
@router.get("/unpaid", response_model=List[schemas.InvoiceOut])
def get_paid_invoice(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    invoice = (
        db.query(models.Invoice)
        .filter(models.Invoice.deleted != True, models.Invoice.paid != True)
        .all()
    )

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no unpaid invoice found",
        )

    return invoice


# unpaid invoice for a user
@router.get("/unpaid/{id}", response_model=List[schemas.InvoiceOut])
def get_paid_invoice_for_specific_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    invoice = (
        db.query(models.Invoice)
        .filter(
            models.Invoice.deleted != True,
            models.Invoice.paid != True,
            models.Invoice.invoice_owner_id == id,
        )
        .all()
    )

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no unpaid invoice found",
        )

    return invoice


# paid invoice for a user
@router.get("/paid/{id}", response_model=List[schemas.InvoiceOut])
def get_unpaid_invoice_for_specific_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    invoice = (
        db.query(models.Invoice)
        .filter(
            models.Invoice.deleted != True,
            models.Invoice.paid != True,
            models.Invoice.invoice_owner_id == id,
        )
        .all()
    )

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no unpaid invoice found",
        )

    return invoice


@router.get("/container/{id}", response_model=List[schemas.ProductOut])
def get_container_prod(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # verify if the container exist
    existence = (
        db.query(models.Category)
        .filter(models.Category.id == id, models.Category.deleted != True)
        .first()
    )
    if existence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"container with id: {id} was not found",
        )

    products = (
        db.query(models.Product)
        .filter(models.Product.container_id == id, models.Category.deleted != True)
        .all()
    )

    if not products:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="this container has no products for now",
        )

    return products


# get product of each category


@router.get("/category/{id}", response_model=List[schemas.ProductOut])
def get_category_prod(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # verify if the container exist
    existence = (
        db.query(models.Category)
        .filter(models.Category.id == id, models.Category.deleted != True)
        .first()
    )
    if existence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"category with id: {id} was not found",
        )

    products = (
        db.query(models.Product)
        .filter(models.Product.category_id == id, models.Category.deleted != True)
        .all()
    )

    if not products:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="this category has no products for now",
        )

    return products


# paid invoice for a user
@router.get("/pay/{id}", response_model=schemas.InvoiceOut)
def mark_as_paid(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    invoice_query = db.query(models.Invoice).filter(
        models.Invoice.id == id, models.Invoice.deleted != True
    )

    invoice = invoice_query.first()
    due = invoice.payment_due
    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"invoice with id: {id} does not exist",
        )
    invoice.paid = True
    invoice.payment_due = 0
    invoice.actual_payment = invoice.value_net
    db.commit()
    db.refresh(invoice)
    sub = due
    up = (
        db.query(models.Magasin)
        .filter(models.Magasin.gerant_id == current_user.id)
        .first()
    )
    if not up:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem")
    up.montant += sub
    db.commit()

    return invoice
