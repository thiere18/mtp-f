"""role and client table

Revision ID: ab878efd72d4
Revises: c10103d826fe
Create Date: 2022-01-02 21:06:15.222939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ab878efd72d4"
down_revision = "c10103d826fe"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "clients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "deleted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("False"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():

    # op.drop_table("roles")
    op.drop_table("clients")
    # op.drop_column("users",'role_id')
