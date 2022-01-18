from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Dict, List, Optional

from pydantic.types import conint
from sqlalchemy import orm

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
class Magasins(BaseModel):
    name: str
    class Config:
        orm_mode = True
class DepenseOut(Depense):
    id: int
    created_at: datetime
    magasin:Magasins
    
    
    class Config:
        orm_mode = True
class MagasinOutDepense(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True
class DepenseOutMagasin(Depense):
    id: int
    created_at: datetime
    magasin:MagasinOutDepense
    class Config:
        orm_mode = True   
# magasin schemas

class Magasin(BaseModel):
    name: str
    montant:int 

class MagasinCreate(Magasin):
    pass
class InvoiceOutMagasin(BaseModel):
    id:int
    reference:str
    value_net: int
    payment_due: int
    actual_payment: int
    invoice_owner_id:int
    paid:bool
    created_at: datetime
    items:List[Dict]
    class Config:
        orm_mode = True
 
class MagasinOut(Magasin):
    id: int
    created_at: datetime
    depenses:List[DepenseOut]
    invoices:List[InvoiceOutMagasin]
    class Config:
        orm_mode = True 
# category schemas

class Category(BaseModel):
    name: str
class ProductsCategory(BaseModel):
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
class CategoryOut(Category):
    id: int
    created_at: datetime
    products:List[ProductsCategory]
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

class Products(BaseModel):
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
class DepotOut(BaseModel):
    id: int
    name: str
    products:List[Products]

    
    class Config:
        orm_mode = True
class ContainerDetails(BaseModel):
    id: int
    reference:str
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
    category_id: int
    container_id: int
    depot_id:int
    container_id:int
    # category:Category
    category:CategoryOut
    container:ContainerDetails
    depot:DepotOut
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
    container_id: int
    depot_id: int
    
# user schemas      

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role_id:int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    permission: str

class TokenData(BaseModel):
    id: Optional[str] = None
class InvoiceOutUser(BaseModel):
    id:int
    reference:str
    value_net: int
    payment_due: int
    actual_payment: int
    invoice_owner_id:int
    paid:bool
    created_at: datetime
    items:List[Dict]
    class Config:
        orm_mode = True
class UserOutForRole(BaseModel):
    id: int
    username: str
    email: EmailStr
    class Config:
        orm_mode = True
    
class RoleCreate(BaseModel):
    name: str


class RoleOut(RoleCreate):
    id: int
    created_at: datetime
    users:List[UserOutForRole]
    class Config:
        orm_mode = True
class RoleUpdate(RoleCreate):
    pass

class RoleOutForUser(RoleCreate):
    id: int
    class Config:
        orm_mode = True
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    role:RoleOutForUser
    # invoices:List[InvoiceOutUser]
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
    products:List[Products]
    class Config:
        orm_mode= True

# class DepotOutC(BaseModel):
#     id: int
#     name: str
#     created_at: datetime
#     products:List[Product]
    
    # class Config:
    #     orm_mode = True
    
# invoice schemas
# class InvoiceItem(BaseModel):
#     product_name:str
#     quantity:int
#     prix_unit:int
# class InvoiceItemOut(BaseModel):
#     id:int
#     product_name:str
#     quantity:int
#     prix_unit:int
#     created_at:datetime
#     class Config:
#         orm_mode = True
 
    
class Invoice(BaseModel):
    reference:str
    value_net: int
    actual_payment: int
    magasin_id:int
    items:List[Dict]
    pass

class InvoiceCreate(Invoice):
    pass

class UserBasic(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True
class InvoiceOut(BaseModel):
    id:int
    reference:str
    value_net: int
    payment_due: int
    actual_payment: int
    invoice_owner_id:int
    paid:bool
    created_at: datetime
    items:List[Dict]
    magasin:MagasinOutDepense
    owner:UserBasic
    class Config:
        orm_mode = True

    pass
class InvoiceDetails(InvoiceOut):
    items:List[Dict]
    
    
class InvDet(BaseModel):
    id: int
    reference:str
    paid:bool
    
    class Config:
        orm_mode = True
    
class UserInvoices(BaseModel):
    id: int
    username:str
    email: EmailStr
    created_at: datetime
    invoices:List[InvDet]
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
class ClientOuts(BaseModel):
    id: int
    name: str
    phone: int
    class Config:
        orm_mode= True

    
class DetteOut(Dette):
    id: int
    created_at: datetime
    dette_owner_id:int
    owner:ClientOuts
    class Config:
        orm_mode = True   
    
    
class DetteOuts(Dette):
    id: int
    created_at: datetime
    # dette_owner_id:int
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
    dettes:List[DetteOuts]
    class Config:
        orm_mode = True
        

class UpdatePassword(BaseModel):
    actual_password: str
    new_password: str
    

class InvoiceUpdate(BaseModel):
    reference:str
    value_net: int
    actual_payment: int
    magasin_id:int
    paid:bool
    items:List[Dict]
    
    