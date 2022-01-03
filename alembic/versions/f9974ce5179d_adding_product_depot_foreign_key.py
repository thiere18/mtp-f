"""adding product_depot foreign key

Revision ID: f9974ce5179d
Revises: 4ced65cd75d2
Create Date: 2021-11-20 17:27:37.326706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9974ce5179d'
down_revision = '4ced65cd75d2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('products', sa.Column('depot_id', sa.Integer(), nullable=False))
    op.create_foreign_key('depot_product_fk', source_table="products", referent_table="depots", local_cols=[
                          'depot_id'], remote_cols=['id'], ondelete="CASCADE")
    


def downgrade():
    op.drop_column("products",'depot_id')
    
