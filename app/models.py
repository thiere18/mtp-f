from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, BigInteger
from .database import Base

class Container(Base):
    __tablename__ = "containers"
    id = Column(Integer, primary_key=True, nullable=False)
    reference = Column(String(255), nullable=False)
    prix_achat = Column(BigInteger(), nullable=False)
    prix_transport = Column(BigInteger(), nullable=False)
    frais_dedouanement = Column(BigInteger(), nullable=False)
    charge_local = Column(BigInteger(), nullable=False)
    dechargement = Column(BigInteger(), nullable=False)
    frais_voyage = Column(BigInteger(), nullable=False)
    total = Column(BigInteger(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)
    products = relationship("Product", back_populates="container")
    pass

class Product(Base):
    __tablename__ = "products"
    id= Column(Integer, primary_key=True, nullable=False)
    reference = Column(String, nullable=False)
    designation = Column(String, nullable=False)
    prix_achat= Column(BigInteger(), nullable=False)
    frais= Column(BigInteger(), nullable=False)
    prix_revient = Column(BigInteger(), nullable=False)
    prix_en_gros = Column(BigInteger(), nullable=False)
    prix_magasin = Column(BigInteger(), nullable=False)
    quantity_per_carton = Column(Integer(), nullable=False)
    quantity_init= Column(Integer(), nullable=True)
    quantity_left= Column(Integer(), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    
    container_id = Column(Integer, ForeignKey("containers.id", ondelete="CASCADE"), nullable=False)
    
    depot_id= Column(Integer, ForeignKey("depots.id", ondelete="CASCADE"),nullable=False)
    category= relationship("Category", back_populates="products")
    container = relationship("Container", back_populates="products")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)

    products= relationship("Product", back_populates="category")

class Depot(Base):
    __tablename__ = "depots"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)
    
    products=relationship("Product",backref="prodep")

    pass


class Magasin(Base):
    __tablename__ = "magasins"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    montant = Column(BigInteger(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)
    gerant_id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    depenses=relationship("Depense",backref="magasin_depense")
    pass

class Depense(Base):
    __tablename__ = "depenses"
    id = Column(Integer, primary_key=True, nullable=False)
    motif = Column(String(255), nullable=False)
    montant = Column(BigInteger(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)
    magasin_id=Column(Integer, ForeignKey(
        "magasins.id", ondelete="CASCADE"), nullable=False)
    pass

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, nullable=False)
    reference = Column(String(255), nullable=False)
    value_net= Column(BigInteger(), nullable=False)
    actual_payment = Column(BigInteger(), nullable=False)
    payment_due = Column(BigInteger(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    paid = Column(Boolean, server_default='False', nullable=False)
    deleted = Column(Boolean, server_default='False', nullable=False)
    magasin_id= Column(Integer, ForeignKey(
        "magasins.id", ondelete="CASCADE"), nullable=False)
    invoice_owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    items=relationship("InvoiceItem",backref="owner")
    pass

class InvoiceItem(Base):
    __tablename__ = "invoiceitems"
    id = Column(Integer, primary_key=True, nullable=False)
    product_name = Column(String(255), nullable=False)
    quantity= Column(Integer(), nullable=False)
    prix_unit= Column(BigInteger(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)
    invoice_id = Column(Integer, ForeignKey(
        "invoices.id", ondelete="CASCADE"), nullable=False)
    


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    invoices=relationship("Invoice",backref="creator")

class Dette(Base):
    __tablename__="dettes"
    id = Column(Integer, primary_key=True, nullable=False)
    reference = Column(String(255), nullable=False)
    total_amount = Column(BigInteger(), nullable=False)
    avance_amount = Column(BigInteger(), nullable=False)
    payment_due = Column(BigInteger(), nullable=False)
    start_date = Column(Date(), nullable=False)
    end_date = Column(Date(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)
    dette_owner_id = Column(Integer, ForeignKey(
        "clients.id", ondelete="CASCADE"), nullable=False)
 
 
class Client(Base):
     __tablename__ = "clients"
     id = Column(Integer, primary_key=True, nullable=False)
     name = Column(String(255), nullable=False)
     phone = Column(String(255), nullable=False)
     created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
     deleted = Column(Boolean, server_default='False', nullable=False)
     dettes=relationship("Dette",backref="owner")
