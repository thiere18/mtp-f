from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

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
    created_at: datetime
    product:ProductOut
    class Config:
        orm_mode= True
    
