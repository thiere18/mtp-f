"""adding foreign key invoice

Revision ID: f3e8868915bd
Revises: b0f73eec3a5f
Create Date: 2021-11-18 06:33:35.787015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3e8868915bd'
down_revision = 'b0f73eec3a5f'
branch_labels = None
depends_on = None


def upgrade():
    
    op.add_column('invoiceitems', sa.Column('invoice_id', sa.Integer(), nullable=False))
    op.create_foreign_key('invoiceitems_invoice_fk', source_table="invoiceitems", referent_table="invoices", local_cols=[
                          'invoice_id'], remote_cols=['id'], ondelete="CASCADE")
    op.add_column('products', sa.Column('category_id', sa.Integer(), nullable=False))
    op.create_foreign_key('products_category_fk', source_table="products", referent_table="categories", local_cols=[
                          'category_id'], remote_cols=['id'], ondelete="CASCADE")
    op.add_column('products', sa.Column('container_id', sa.Integer(), nullable=False))
    op.create_foreign_key('products_container_fk', source_table="products", referent_table="containers", local_cols=[
                          'container_id'], remote_cols=['id'], ondelete="CASCADE")
    
    pass


def downgrade():
    pass
