"""add_last_few_columns_to_posts_table.py

Revision ID: 4af94e06e9d9
Revises: a4a5ac6b03c0
Create Date: 2025-05-17 13:05:49.389327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4af94e06e9d9'
down_revision: Union[str, None] = 'a4a5ac6b03c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('Now()') ),)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
