"""dette tables

Revision ID: 6eea7adb91d5
Revises: ab878efd72d4
Create Date: 2022-01-18 20:09:06.562821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eea7adb91d5'
down_revision = 'ab878efd72d4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('dettes',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('reference', sa.String(), nullable=False),
                    sa.Column('total_amount', sa.Integer(), nullable=False),
                    sa.Column('avance_amount', sa.Integer(), nullable=False),
                    sa.Column('payment_due', sa.Integer(), nullable=False),
                    sa.Column('start_date', sa.DateTime(), nullable=False),
                    sa.Column('end_date', sa.DateTime(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('deleted', sa.Boolean(), nullable=False,
                            server_default=sa.text('False'),
                              ),
                    sa.Column('owner_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    )
    op.create_foreign_key('dette_client_fk', source_table="dettes", referent_table="clients", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")

    pass


def downgrade():
    pass
