from fastapi import Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repository import invoice
# from sqlalchemy.sql.functions import func
from .. import schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/invoices",
    tags=['Invoices']
)

@router.get("/", response_model=List[schemas.InvoiceOut])
def get_invoices(response: Response,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):
    return  invoice.get_invoices(response,db)

@router.get("/", response_model=List[schemas.InvoiceOut])
def get_invoices(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),search: Optional[str] = ""):
    return invoice.get_invoices(db,search)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.InvoiceOut)
async def create_invoice(post: schemas.InvoiceCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return invoice.create_invoice(post, db)

@router.get("/{id}", response_model=schemas.InvoiceOut)
def get_invoice(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return invoice.get_invoice(id, db)

@router.put("/{id}", response_model=schemas.InvoiceOut)
def update_invoice(id: int, updated_post: schemas.InvoiceUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return invoice.get_invoice(id,updated_post,db)

@router.delete("/{id}",response_model_exclude_none=True)
def delete_invoice(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return invoice.delete_invoice(id, db) 
#Response(status_code=status.HTTP_204_NO_CONTENT)


