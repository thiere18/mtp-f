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

class DepotOut(BaseModel):
    id: int
    name: str
    created_at: datetime
    class Config:
        orm_mode = True

class DepotCreate(Depot):
    pass
# magasin schemas

class Magasin(BaseModel):
    name: str
    montant:int
    
class MagasinOut(BaseModel):
    id: int
    name: str
    montant: int
    created_at: datetime
    class Config:
        orm_mode = True
    
class MagasinCreate(Magasin):
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
    prix_revient:int
    prix_en_gros: int
    prix_magasin:int
    quantity_per_carton: int
    quantity_init: int
    quantity_left:int
    category_id: int
    container_id: int
    
    
    


class ProductCreate(Product):
    pass

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
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


class ContainerOut(BaseModel):
    id: int
    reference:str
    prix_achat:int
    prix_transport:int
    frais_dedouanement: int
    charge_local: int
    dechargement: int
    frais_voyage: int
    created_at: datetime
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
    category:CategoryOut
    container:ContainerOut
    class Config:
        orm_mode = True
    
class Cont(ContainerOut):
    products:List[ProductOut]
    class Config:
        orm_mode = True
    
# invoice schemas
class InvoiceItem(BaseModel):
    product_name:str
    quantity:int
    prix_unit:int
class InvoiceItemOut(InvoiceItem):
    id:int
    created_at:datetime
    class Config:
        orm_mode = True
    
class Invoice(BaseModel):
    reference:str
    value_net: int
    actual_payment: int
    payment_due: int
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
    created_at: datetime
    # own:InvoiceItemOut
    class Config:
        orm_mode = True

    pass
class InvoiceDetails(InvoiceOut):
    items:list[InvoiceItem]