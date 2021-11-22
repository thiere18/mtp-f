from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
    





  
    
    # depot schemas
class Depot(BaseModel):
    name: str


class DepotCreate(Depot):
    pass
# magasin schemas

class Magasin(BaseModel):
    name: str
    montant:int
    
class Depense(BaseModel):
    motif: str
    montant:int
    magasin_id: int

 
class DepenseOut(BaseModel):
    id: int
    motif: str
    montant: int
    created_at: datetime
    class Config:
        orm_mode = True
        
class MagasinOut(BaseModel):
    id: int
    name: str
    montant: int
    created_at: datetime
    depenses:List[DepenseOut]
    class Config:
        orm_mode = True
    

        
class Depensecreate(Depense):
    pass

class MagasinCreate(Magasin):
    pass

class Depensecreate(Depense):
    pass

# category schemas

class Category(BaseModel):
    name: str

class CategoryOut(BaseModel):
    id: int
    name: str
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

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
        
#user schemas      


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


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
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
    
class Cont(ContainerOut):
    products:List[ProductOut]
    class Config:
        orm_mode = True
        
    
class DepotOut(BaseModel):
    id: int
    name: str
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
    items:list[InvoiceItem]
    
    
class UserInvoices(BaseModel):
    # id: int
    username:str
    email: EmailStr
    created_at: datetime
    invoices:list[InvoiceOut]
    class Config:
        orm_mode = True
        
        
