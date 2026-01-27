"""add last columns to posts table

Revision ID: 1b73bee4774b
Revises: 0ac2d9d6c3f7
Create Date: 2026-01-27 00:11:01.778529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b73bee4774b'
down_revision: Union[str, Sequence[str], None] = '0ac2d9d6c3f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts' ,sa.Column(
        'published' , sa.Boolean() , nullable=False  , server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at' , sa.TIMESTAMP(timezone=True) , nullable=False , server_default=sa.text('NOW()'),))
    pass


def downgrade():
    op.drop_columns('posts' , 'published')
    op.drop_column('posts' , 'created_at')
    pass
