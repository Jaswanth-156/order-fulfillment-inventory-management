from alembic import op


# revision identifiers, used by Alembic.
revision = "641075661bc6"
down_revision = "87662b7bc508"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        INSERT INTO categories (name, description)
        SELECT 'Electronics', 'Electronic products'
        WHERE NOT EXISTS (
            SELECT 1
            FROM categories
            WHERE name = 'Electronics'
        )
        """
    )


def downgrade():
    op.execute(
        """
        DELETE FROM categories
        WHERE name = 'Electronics'
        """
    )