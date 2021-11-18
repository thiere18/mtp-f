"""depot tables

Revision ID: 9b7f0314cc34
Revises: c8891c1f6abf
Create Date: 2021-11-17 16:40:01.601895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b7f0314cc34'
down_revision = 'c8891c1f6abf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('depots',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('deleted', sa.Boolean(), nullable=False,
                            server_default=sa.text('False'),
                              ),
                    
                    sa.PrimaryKeyConstraint('id'),
                    )
    pass


def downgrade():
    op.drop_table('depots')
    pass
