"""add_office_id_to_users

Revision ID: a1b2c3d4e5f6
Revises: 75e96389dec1
Create Date: 2025-12-02 17:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '75e96389dec1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add office_id column to users table
    op.add_column('users', sa.Column('office_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_users_office_id',
        'users', 'offices',
        ['office_id'], ['id']
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove office_id column from users table
    op.drop_constraint('fk_users_office_id', 'users', type_='foreignkey')
    op.drop_column('users', 'office_id')

