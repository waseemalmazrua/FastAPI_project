""" create posts table

Revision ID: 131f3c82b0c9
Revises: 
Create Date: 2026-01-26 15:00:28.678601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '131f3c82b0c9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts' , sa.Column('id',sa.Integer() , nullable=False , primary_key=True),
                    sa.Column('title' , sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
