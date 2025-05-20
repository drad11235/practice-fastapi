"""add content column to posts table

Revision ID: 8c2246435a6c
Revises: edd0f514cc12
Create Date: 2025-05-17 11:54:20.361616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c2246435a6c'
down_revision: Union[str, None] = 'edd0f514cc12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
