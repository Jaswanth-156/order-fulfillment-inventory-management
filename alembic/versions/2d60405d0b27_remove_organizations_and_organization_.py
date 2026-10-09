"""remove organizations and organization from users

Revision ID: 2d60405d0b27
Revises: 12fa66889c46
Create Date: 2026-09-28

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2d60405d0b27"
down_revision: Union[str, Sequence[str], None] = "12fa66889c46"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove foreign key from users
    op.drop_constraint(
        "fk_users_organization_id",
        "users",
        type_="foreignkey"
    )

    # Remove organization_id from users
    op.drop_column(
        "users",
        "organization_id"
    )

    # Remove organizations table
    op.drop_table("organizations")


def downgrade() -> None:
    # Re-create organizations table
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name")
    )

    # Re-create organization_id
    op.add_column(
        "users",
        sa.Column(
            "organization_id",
            sa.Integer(),
            nullable=True
        )
    )

    # Re-create foreign key
    op.create_foreign_key(
        "fk_users_organization_id",
        "users",
        "organizations",
        ["organization_id"],
        ["id"]
    )