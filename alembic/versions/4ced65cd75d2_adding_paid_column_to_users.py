"""adding paid column to users

Revision ID: 4ced65cd75d2
Revises: 564f17457e23
Create Date: 2021-11-20 16:18:10.452328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ced65cd75d2'
down_revision = '564f17457e23'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('username', sa.String(), nullable=False))


def downgrade():
    op.drop_column('users','username')

