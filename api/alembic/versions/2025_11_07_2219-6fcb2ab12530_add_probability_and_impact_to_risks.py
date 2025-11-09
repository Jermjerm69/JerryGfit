"""add probability and impact to risks

Revision ID: 6fcb2ab12530
Revises: a1b2c3d4e5f6
Create Date: 2025-11-07 22:19:01.757554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fcb2ab12530'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enum types first
    op.execute("CREATE TYPE riskprobability AS ENUM ('low', 'medium', 'high')")
    op.execute("CREATE TYPE riskimpact AS ENUM ('low', 'medium', 'high', 'critical')")

    # Add probability and impact columns to risks table
    op.add_column('risks', sa.Column('probability', sa.Enum('low', 'medium', 'high', name='riskprobability'), nullable=False, server_default='medium'))
    op.add_column('risks', sa.Column('impact', sa.Enum('low', 'medium', 'high', 'critical', name='riskimpact'), nullable=False, server_default='medium'))


def downgrade() -> None:
    # Remove probability and impact columns from risks table
    op.drop_column('risks', 'impact')
    op.drop_column('risks', 'probability')
    # Drop the enum types
    op.execute('DROP TYPE IF EXISTS riskimpact')
    op.execute('DROP TYPE IF EXISTS riskprobability')
