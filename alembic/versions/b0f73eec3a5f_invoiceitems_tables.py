"""invoiceItems tables

Revision ID: b0f73eec3a5f
Revises: ff58fd21cc27
Create Date: 2021-11-17 23:16:50.839859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0f73eec3a5f'
down_revision = 'ff58fd21cc27'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('invoiceitems', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('product_name', sa.String(), nullable=False),
                    sa.Column('quantity',sa.Integer(),nullable=False),
                    sa.Column('prix_unit',sa.BigInteger(),nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('deleted', sa.Boolean(), default=False),
                    sa.PrimaryKeyConstraint('id'),
                    )
    pass


def downgrade():
    pass
