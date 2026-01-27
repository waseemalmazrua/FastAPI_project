"""add content column to posts table

Revision ID: a23e63ec9817
Revises: 131f3c82b0c9
Create Date: 2026-01-26 16:26:08.148716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a23e63ec9817'
down_revision: Union[str, Sequence[str], None] = '131f3c82b0c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(): 
    op.add_column('posts' , sa.Column('content' , sa.String() , nullable=False))
    pass


def downgrade():
    op.drop_table('posts' , 'content')

    pass
