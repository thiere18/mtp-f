"""products tables

Revision ID: a53bdbfea521
Revises: 9b7f0314cc34
Create Date: 2021-11-17 17:29:10.612332

"""
from re import T
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a53bdbfea521"
down_revision = "9b7f0314cc34"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("reference", sa.String(), nullable=False),
        sa.Column("designation", sa.String(), nullable=False),
        sa.Column("prix_achat", sa.BigInteger(), nullable=False),
        sa.Column("frais", sa.BigInteger(), nullable=False),
        sa.Column("prix_revient", sa.BigInteger(), nullable=False),
        sa.Column("prix_en_gros", sa.BigInteger(), nullable=False),
        sa.Column("prix_magasin", sa.BigInteger(), nullable=False),
        sa.Column("quantity_per_carton", sa.Integer(), nullable=False),
        sa.Column("quantity_left", sa.Integer(), nullable=True),
        sa.Column("quantity_init", sa.Integer(), nullable=True),
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
    op.drop_table("products")
