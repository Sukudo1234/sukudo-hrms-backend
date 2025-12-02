"""remove_remote_column_from_offices

Revision ID: 75e96389dec1
Revises: 
Create Date: 2025-12-02 16:10:24.997024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75e96389dec1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the remote column from offices table
    op.drop_column('offices', 'remote')


def downgrade() -> None:
    """Downgrade schema."""
    # Add back the remote column to offices table
    op.add_column('offices', sa.Column('remote', sa.Boolean(), nullable=False, server_default='false'))
