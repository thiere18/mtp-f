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
    pass
