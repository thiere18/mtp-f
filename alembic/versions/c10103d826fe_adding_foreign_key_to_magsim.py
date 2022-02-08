"""adding foreign key to magsim

Revision ID: c10103d826fe
Revises: c58318a393ee
Create Date: 2021-11-20 18:29:06.822270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c10103d826fe"
down_revision = "c58318a393ee"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("invoices", sa.Column("magasin_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "magasin_invoice_fk",
        source_table="invoices",
        referent_table="magasins",
        local_cols=["magasin_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    op.create_table(
        "depenses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("motif", sa.String(), nullable=False),
        sa.Column("montant", sa.BigInteger(), nullable=False),
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
        sa.Column("magasin_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_foreign_key(
        "magasin_depense_fk",
        source_table="depenses",
        referent_table="magasins",
        local_cols=["magasin_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_table("depenses")
