"""magasin tables

Revision ID: 896cbc45acbf
Revises: a53bdbfea521
Create Date: 2021-11-17 17:30:12.832742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '896cbc45acbf'
down_revision = 'a53bdbfea521'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('magasins', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('montant', sa.BigInteger(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('deleted', sa.Boolean(), default=False),
                    sa.PrimaryKeyConstraint('id'),

                    )
    pass


def downgrade():
    op.drop_table('magasins')
    pass
