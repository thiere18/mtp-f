from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, BigInteger

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


# class Vote(Base):
#     __tablename__ = "votes"
#     user_id = Column(Integer, ForeignKey(
#         "users.id", ondelete="CASCADE"), primary_key=True)
#     post_id = Column(Integer, ForeignKey(
#         "posts.id", ondelete="CASCADE"), primary_key=True)

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
    
    category_id = Column(Integer, ForeignKey(
        "categories.id", ondelete="CASCADE"), nullable=False)
    
    container_id = Column(Integer, ForeignKey(
        "containers.id", ondelete="CASCADE"), nullable=False
    )
    
    container=relationship("Containers")
    category= relationship("Category")
    
    pass

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)


class Depot(Base):
    __tablename__ = "depots"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)

    pass

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
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)

    pass

class Magasin(Base):
    __tablename__ = "magasins"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    montant = Column(BigInteger(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)

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
    deleted = Column(Boolean, server_default='False', nullable=False)
    invoice_owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    user_invoices=relationship("User")
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
    my_invoice=relationship("Items")