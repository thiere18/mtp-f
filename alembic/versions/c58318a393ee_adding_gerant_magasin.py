"""adding gerant magasin

Revision ID: c58318a393ee
Revises: 56d6a44844d6
Create Date: 2021-11-20 18:15:39.086118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c58318a393ee'
down_revision = '56d6a44844d6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('magasins',sa.Column('gerant_id',sa.Integer(), nullable=False))
    op.create_foreign_key('magasin_gerant_fk', source_table="magasins", referent_table="users", local_cols=[
                          'gerant_id'], remote_cols=['id'], ondelete="CASCADE")
    


def downgrade():
    pass