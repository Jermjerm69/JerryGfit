"""add user roles

Revision ID: b9c8d4e5f7g8
Revises: a67d7e971965
Create Date: 2025-11-09 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9c8d4e5f7g8'
down_revision = 'a67d7e971965'
branch_labels = None
depends_on = None


def upgrade():
    # Add role column to users table
    op.add_column('users', sa.Column('role', sa.String(), nullable=False, server_default='user'))

    # Create index on role column
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)


def downgrade():
    # Drop index
    op.drop_index(op.f('ix_users_role'), table_name='users')

    # Drop role column
    op.drop_column('users', 'role')
