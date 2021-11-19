"""invoice tables

Revision ID: ff58fd21cc27
Revises: 89f345fbe751
Create Date: 2021-11-17 17:30:50.256862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff58fd21cc27'
down_revision = '89f345fbe751'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('invoices', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('reference', sa.String(), nullable=False),
                    sa.Column('value_net', sa.BigInteger(), nullable=False),
                    sa.Column('actual_payment',sa.BigInteger(), nullable=False),
                    sa.Column('payment_due',sa.BigInteger(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('deleted', sa.Boolean(), nullable=False,server_default=sa.text('False'),),
                    sa.PrimaryKeyConstraint('id'),

                    )
    pass


def downgrade():
    pass
