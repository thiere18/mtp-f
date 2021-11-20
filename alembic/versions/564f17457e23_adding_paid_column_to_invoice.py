"""adding paid column to invoice

Revision ID: 564f17457e23
Revises: f3e8868915bd
Create Date: 2021-11-20 13:17:36.255472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '564f17457e23'
down_revision = 'f3e8868915bd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('invoices', sa.Column('paid', sa.Boolean(), nullable=False,server_default=sa.text('False')))
    pass


def downgrade():   
    pass