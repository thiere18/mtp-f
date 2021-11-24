from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

from pydantic.types import conint

    # depot schemas
class Depot(BaseModel):
    name: str

class DepotCreate(Depot):
    pass

# depense schemas
class Depense(BaseModel):
    motif: str
    montant:int
    magasin_id: int

class Depensecreate(Depense):
    pass

class DepenseOut(Depense):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True
      
# magasin schemas

class Magasin(BaseModel):
    name: str
    montant:int 

class MagasinCreate(Magasin):
    pass
  
class MagasinOut(Magasin):
    id: int
    created_at: datetime
    depenses:List[DepenseOut]
    class Config:
        orm_mode = True 
# category schemas

class Category(BaseModel):
    name: str

class CategoryOut(Category):
    id: int
    created_at: datetime
    class Config:
        orm_mode= True
    
class CategoryCreate(Category):
    pass
    
#product schemas

class Product(BaseModel):
    reference:str
    designation: str
    prix_achat:int
    frais: int
    prix_en_gros: int
    prix_magasin:int
    quantity_per_carton: int
    quantity_init: int
    category_id: int
    depot_id: int
    container_id: int
    
class ProductCreate(Product):
    pass

class Product(BaseModel):
    id: int
    reference:str
    designation: str
    prix_achat:int
    frais: int
    prix_revient:int
    prix_en_gros: int
    prix_magasin:int
    quantity_per_carton: int
    quantity_init: int
    quantity_left:int
    created_at: datetime
    class Config:
        orm_mode = True
        
class ProductOut(BaseModel):
    id: int
    reference:str
    designation: str
    prix_achat:int
    frais: int
    prix_revient:int
    prix_en_gros: int
    prix_magasin:int
    quantity_per_carton: int
    quantity_init: int
    quantity_left:int
    created_at: datetime
    category:Category
    class Config:
        orm_mode = True
    
class ProductCont(BaseModel):
    reference:str
    designation: str
    prix_achat:int
    frais: int
    prix_en_gros: int
    prix_magasin:int
    quantity_per_carton: int
    quantity_init: int
    category_id: int
    depot_id: int
    
# user schemas      

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True  

# container schemas
class Container(BaseModel):
    reference:str
    prix_achat:int
    prix_transport:int
    frais_dedouanement: int
    charge_local: int
    dechargement: int
    frais_voyage: int
    
class ContainerCreate(Container):
    pass


class ContainerOut(BaseModel):
    id: int
    reference:str
    prix_achat:int
    prix_transport:int
    frais_dedouanement: int
    charge_local: int
    dechargement: int
    frais_voyage: int
    total: int
    created_at: datetime
    products:List[Product]
    class Config:
        orm_mode= True

class DepotOut(Depot):
    id: int
    created_at: datetime
    products:List[Product]
    
    class Config:
        orm_mode = True
    
# invoice schemas
class InvoiceItem(BaseModel):
    product_name:str
    quantity:int
    prix_unit:int
class InvoiceItemOut(BaseModel):
    id:int
    product_name:str
    quantity:int
    prix_unit:int
    created_at:datetime
    class Config:
        orm_mode = True
    
class Invoice(BaseModel):
    reference:str
    value_net: int
    actual_payment: int
    magasin_id:int
    pass

class InvoiceCreate(Invoice):
    pass

class InvoiceOut(BaseModel):
    id:int
    reference:str
    value_net: int
    payment_due: int
    actual_payment: int
    invoice_owner_id:int
    paid:bool
    created_at: datetime
    items:List[InvoiceItemOut]
    class Config:
        orm_mode = True

    pass
class InvoiceDetails(InvoiceOut):
    items:List[InvoiceItem]
    
    
class UserInvoices(BaseModel):
    # id: int
    username:str
    email: EmailStr
    created_at: datetime
    invoices:List[InvoiceOut]
    class Config:
        orm_mode = True
        
        
# fournisseur schemas


# dettes schemas

class Dette(BaseModel):
    reference :str
    total_amount:int
    avance_amount: int
    payment_due: int
    start_date: datetime
    end_date: datetime
    
class DetteCreate(Dette):
    pass

    
class DetteOut(Dette):
    id: int
    created_at: datetime
    dette_owner_id:int
    class Config:
        orm_mode = True   
        
# client SQLALCHEMY_DATABASE_URL

class Client(BaseModel):
    name: str
    phone: int

class ClientCreate(Client):
    pass

class ClientOut(Client):
    created_at: datetime
    dettes:List[DetteOut]
    class Config:
        orm_mode = True
        
    
