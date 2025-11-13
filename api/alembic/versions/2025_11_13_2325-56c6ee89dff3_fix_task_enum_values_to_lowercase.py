"""fix_task_enum_values_to_lowercase

Revision ID: 56c6ee89dff3
Revises: 0d5a93280518
Create Date: 2025-11-13 23:25:06.237332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56c6ee89dff3'
down_revision = '0d5a93280518'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create new enum types with lowercase values
    op.execute("CREATE TYPE taskstatus_new AS ENUM ('todo', 'in_progress', 'done', 'blocked')")
    op.execute("CREATE TYPE taskpriority_new AS ENUM ('low', 'medium', 'high', 'urgent')")

    # Convert columns to use new enum types with lowercase values
    op.execute("""
        ALTER TABLE tasks
        ALTER COLUMN status TYPE taskstatus_new
        USING LOWER(status::text)::taskstatus_new
    """)
    op.execute("""
        ALTER TABLE tasks
        ALTER COLUMN priority TYPE taskpriority_new
        USING LOWER(priority::text)::taskpriority_new
    """)

    # Drop old enum types
    op.execute("DROP TYPE taskstatus")
    op.execute("DROP TYPE taskpriority")

    # Rename new types to original names
    op.execute("ALTER TYPE taskstatus_new RENAME TO taskstatus")
    op.execute("ALTER TYPE taskpriority_new RENAME TO taskpriority")


def downgrade() -> None:
    # Create old enum types with uppercase values
    op.execute("CREATE TYPE taskstatus_old AS ENUM ('TODO', 'IN_PROGRESS', 'DONE', 'BLOCKED')")
    op.execute("CREATE TYPE taskpriority_old AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'URGENT')")

    # Convert columns back to uppercase enum types
    op.execute("""
        ALTER TABLE tasks
        ALTER COLUMN status TYPE taskstatus_old
        USING UPPER(status::text)::taskstatus_old
    """)
    op.execute("""
        ALTER TABLE tasks
        ALTER COLUMN priority TYPE taskpriority_old
        USING UPPER(priority::text)::taskpriority_old
    """)

    # Drop new enum types
    op.execute("DROP TYPE taskstatus")
    op.execute("DROP TYPE taskpriority")

    # Rename old types to original names
    op.execute("ALTER TYPE taskstatus_old RENAME TO taskstatus")
    op.execute("ALTER TYPE taskpriority_old RENAME TO taskpriority")
