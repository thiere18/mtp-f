"""users tables

Revision ID: d0ff398cbc6c
Revises: 
Create Date: 2021-11-17 16:32:18.505209

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import ForeignKey


# revision identifiers, used by Alembic.
revision = 'd0ff398cbc6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('deleted', sa.Boolean(), nullable=False,server_default=sa.text('False'),),
                    sa.Column('role_id',sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    )
    
    op.create_table('roles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('deleted', sa.Boolean(), nullable=False,
                            server_default=sa.text('False'),
                              ),
                    sa.PrimaryKeyConstraint('id'),
                    )

    # op.add_column('users', sa.Column('role_id', sa.Integer(), nullable=False))
    op.create_foreign_key('user_rol_fk', source_table="users", referent_table="roles", local_cols=[
                          'role_id'], remote_cols=['id'], ondelete="CASCADE")
def downgrade():
    op.drop_table('roles')

    op.drop_table('users')
