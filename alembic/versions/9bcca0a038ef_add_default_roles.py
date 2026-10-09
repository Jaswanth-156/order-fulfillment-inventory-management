"""add default roles

Revision ID: 9bcca0a038ef
Revises: 42d3c0904797
Create Date: 2026-09-28 11:27:44.281325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9bcca0a038ef'
down_revision: Union[str, Sequence[str], None] = '42d3c0904797'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        INSERT INTO roles (name)
        VALUES
            ('Admin'),
            ('Warehouse Manager'),
            ('Fulfillment Agent'),
            ('Customer')
        ON CONFLICT (name) DO NOTHING
    """)


def downgrade():
    op.execute("""
        DELETE FROM roles
        WHERE name IN (
            'Admin',
            'Warehouse Manager',
            'Fulfillment Agent',
            'Customer'
        )
    """)

