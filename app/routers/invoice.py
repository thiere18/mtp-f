from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio
from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/invoices",
    tags=['Invoices']
)

# def add_invoice_item(invoice_ides:int,data:list(),db: Session, current_user: int = Depends(oauth2.get_current_user) ):
#     for invoice_item in data:
#         new_invoice = models.InvoiceItem(invoice_id=invoice_ides,**invoice_item.dict())
#         db.add(new_invoice)
#         db.commit()

@router.get("/", response_model=List[schemas.InvoiceOut])
def get_invoices(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    containers=db.query(models.Invoice).filter(models.Invoice.deleted!=True).all()
    return  containers


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_invoice(post: schemas.InvoiceCreate,item:List[schemas.InvoiceItem], db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    new_invoice = models.Invoice(invoice_owner_id=current_user.id, **post.dict())
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    await asyncio.sleep(1)
    new_id=new_invoice.id
    for invoice_item in item:
        new_invoice = models.InvoiceItem(invoice_id=new_id,**invoice_item.dict())
        db.add(new_invoice)
        db.commit()
    # add_invoice_item(new_invoice.id,item, db=Depends(get_db))
    
    return {"msg": "Invoice added successfully"}



@router.get("/{id}", response_model=schemas.InvoiceOut)
def get_invoice(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  

    invoice = db.query(models.Invoice).filter(models.Invoice.id == id,models.Invoice.deleted!=True).first()

    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"invoice with id: {id} was not found")

    return invoice


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    invoice_query = db.query(models.Invoice).filter(models.Invoice.id == id,models.Invoice.deleted!=True)

    invoice = invoice_query.first()

    if invoice == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"invoice with id: {id} does not exist")
    invoice.deleted = True
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.InvoiceOut)
def update_invoice(id: int, updated_post: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):



    invoice_query = db.query(models.Invoice).filter(models.Invoice.id == id,models.Invoice.deleted!=True)

    invoice = invoice_query.first()

    if invoice == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"invoice with id: {id} does not exist")

    
    invoice_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return invoice_query.first()

@router.get("/detail/{id}", response_model=List[schemas.InvoiceItemOut])
def get_invoice_detail(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  
# verify if the container exist
    existence= db.query(models.Invoice).filter(models.Invoice.id==id,models.Invoice.deleted!=True).first()
    if existence==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"invoice with id: {id} was not found")
         
    items = db.query(models.InvoiceItem).filter(models.InvoiceItem.invoice_id == id,models.InvoiceItem.deleted!=True).all()

    if not items:
         raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"this category has no items for now")
    return items



