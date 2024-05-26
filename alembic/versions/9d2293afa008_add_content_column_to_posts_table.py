"""add content column to posts table

Revision ID: 9d2293afa008
Revises: 885b7303dcbb
Create Date: 2024-05-25 20:20:41.756042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d2293afa008'
down_revision: Union[str, None] = '885b7303dcbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass