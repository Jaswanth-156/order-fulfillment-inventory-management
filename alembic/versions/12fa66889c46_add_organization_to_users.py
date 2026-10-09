"""add organization to users

Revision ID: 12fa66889c46
Revises: a08e0a96152e
Create Date: 2026-09-28 13:28:22.713355

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "12fa66889c46"
down_revision: Union[str, Sequence[str], None] = "a08e0a96152e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add column temporarily as nullable
    op.add_column(
        "users",
        sa.Column(
            "organization_id",
            sa.Integer(),
            nullable=True
        )
    )

    # Create a default organization for existing users
    op.execute(
        """
        INSERT INTO organizations (name, is_active)
        VALUES ('Default Organization', TRUE)
        """
    )

    # Assign the organization to existing users
    op.execute(
        """
        UPDATE users
        SET organization_id = (
            SELECT id
            FROM organizations
            WHERE name = 'Default Organization'
            LIMIT 1
        )
        WHERE organization_id IS NULL
        """
    )

    # Make the column mandatory
    op.alter_column(
        "users",
        "organization_id",
        existing_type=sa.Integer(),
        nullable=False
    )

    # Create foreign key
    op.create_foreign_key(
        "fk_users_organization_id",
        "users",
        "organizations",
        ["organization_id"],
        ["id"]
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_users_organization_id",
        "users",
        type_="foreignkey"
    )

    op.drop_column(
        "users",
        "organization_id"
    )