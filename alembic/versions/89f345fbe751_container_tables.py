"""container tables

Revision ID: 89f345fbe751
Revises: 896cbc45acbf
Create Date: 2021-11-17 17:30:25.307595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89f345fbe751'
down_revision = '896cbc45acbf'
branch_labels = None
depends_on = None


def upgrade():
   op.create_table('containers',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('reference', sa.String(), nullable=False),
                    sa.Column('prix_achat', sa.Integer(), nullable=False),
                    sa.Column('prix_transprot', sa.Integer(), nullable=False),
                    sa.Column('frais_dedouanement',sa.Integer(), nullable=False),
                    sa.Column('charge_local',sa.Integer(), nullable=False),
                    sa.Column('dechargement',sa.Integer(), nullable=False),
                    sa.Column('frais_voyage',sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('deleted', sa.Boolean(), default=False),
                    sa.PrimaryKeyConstraint('id'),
                    )   
   pass


def downgrade():
    op.drop_table('containers')
    pass
