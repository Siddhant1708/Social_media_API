"""add content col to posts table

Revision ID: 7da4d2983436
Revises: af5daa71f66d
Create Date: 2025-09-02 01:27:04.777735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7da4d2983436'
down_revision: Union[str, Sequence[str], None] = 'af5daa71f66d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
