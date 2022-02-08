from fastapi import Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
import asyncio

# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


def get_invoices(
    response: Response,
    db: Session,
):

    invoices = db.query(models.Invoice).filter(models.Invoice.deleted != True).all()
    response.headers["Content-Range"] = f"0-9/{len(invoices)}"
    response.headers["X-Total-Count"] = "30"
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"

    return invoices


def get_invoices(db: Session, search: Optional[str] = ""):

    return (
        db.query(models.Invoice)
        .filter(
            models.Invoice.deleted != True,
            models.Invoice.reference.contains(search),
        )
        .all()
    )


async def create_invoice(
    post: schemas.InvoiceCreate,
    db: Session,
    current_user: int = Depends(oauth2.get_current_user),
):
    for invoice_item in post.items:
        prod = invoice_item.product_name
        quant = invoice_item.quantity
        # verify if this product exist
        p = db.query(models.Product).filter(models.Product.designation == prod).first()
        if not p:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{prod} is not a product",
            )
        p.quantity_left -= quant
        db.commit()
    new_invoice = models.Invoice(
        invoice_owner_id=current_user.id,
        payment_due=(post.value_net - post.actual_payment),
        **post.dict(),
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    sub = new_invoice.actual_payment
    up = (
        db.query(models.Magasin)
        .filter(models.Magasin.gerant_id == current_user.id)
        .first()
    )
    if not up:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem")
    up.montant += sub
    db.commit()
    await asyncio.sleep(1)
    return new_invoice


def get_invoice(id: int, db: Session):

    invoice = (
        db.query(models.Invoice)
        .filter(models.Invoice.id == id, models.Invoice.deleted != True)
        .first()
    )

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"invoice with id: {id} was not found",
        )

    return invoice


def update_invoice(id: int, updated_post: schemas.InvoiceUpdate, db: Session):

    invoice_query = db.query(models.Invoice).filter(
        models.Invoice.id == id, models.Invoice.deleted != True
    )

    invoice = invoice_query.first()

    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"invoice with id: {id} does not exist",
        )

    invoice_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return invoice_query.first()


def delete_invoice(id: int, db: Session):

    invoice_query = db.query(models.Invoice).filter(
        models.Invoice.id == id, models.Invoice.deleted != True
    )

    invoice = invoice_query.first()

    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"invoice with id: {id} does not exist",
        )
    invoice.deleted = True
    db.commit()
    return invoice  # Response(status_code=status.HTTP_204_NO_CONTENT)
