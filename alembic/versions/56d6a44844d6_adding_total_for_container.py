"""adding total for container

Revision ID: 56d6a44844d6
Revises: f9974ce5179d
Create Date: 2021-11-20 17:57:01.412246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56d6a44844d6'
down_revision = 'f9974ce5179d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('containers',sa.Column('total',sa.BigInteger(), nullable=False))
    
    pass


def downgrade():
    pass
