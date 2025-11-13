"""fix_risk_enum_values_to_lowercase

Revision ID: 0d5a93280518
Revises: b9c8d4e5f7g8
Create Date: 2025-11-13 01:49:19.323668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d5a93280518'
down_revision = 'b9c8d4e5f7g8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create new enum types with lowercase values
    op.execute("CREATE TYPE riskseverity_new AS ENUM ('low', 'medium', 'high', 'critical')")
    op.execute("CREATE TYPE riskstatus_new AS ENUM ('open', 'mitigated', 'closed')")

    # Convert columns to use new enum types with lowercase values
    op.execute("""
        ALTER TABLE risks
        ALTER COLUMN severity TYPE riskseverity_new
        USING LOWER(severity::text)::riskseverity_new
    """)
    op.execute("""
        ALTER TABLE risks
        ALTER COLUMN status TYPE riskstatus_new
        USING LOWER(status::text)::riskstatus_new
    """)

    # Drop old enum types
    op.execute("DROP TYPE riskseverity")
    op.execute("DROP TYPE riskstatus")

    # Rename new types to original names
    op.execute("ALTER TYPE riskseverity_new RENAME TO riskseverity")
    op.execute("ALTER TYPE riskstatus_new RENAME TO riskstatus")


def downgrade() -> None:
    # Create old enum types with uppercase values
    op.execute("CREATE TYPE riskseverity_old AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')")
    op.execute("CREATE TYPE riskstatus_old AS ENUM ('OPEN', 'MITIGATED', 'CLOSED')")

    # Convert columns back to uppercase enum types
    op.execute("""
        ALTER TABLE risks
        ALTER COLUMN severity TYPE riskseverity_old
        USING UPPER(severity::text)::riskseverity_old
    """)
    op.execute("""
        ALTER TABLE risks
        ALTER COLUMN status TYPE riskstatus_old
        USING UPPER(status::text)::riskstatus_old
    """)

    # Drop new enum types
    op.execute("DROP TYPE riskseverity")
    op.execute("DROP TYPE riskstatus")

    # Rename old types to original names
    op.execute("ALTER TYPE riskseverity_old RENAME TO riskseverity")
    op.execute("ALTER TYPE riskstatus_old RENAME TO riskstatus")
