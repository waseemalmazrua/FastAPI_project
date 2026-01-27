"""add foreign-key to posts table

Revision ID: 0ac2d9d6c3f7
Revises: f3a2c8fa7a52
Create Date: 2026-01-26 23:22:33.339391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ac2d9d6c3f7'
down_revision: Union[str, Sequence[str], None] = 'f3a2c8fa7a52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts' , sa.Column('owner_id' , sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk' , source_table='posts',referent_table='users' , local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
                
                  

    pass


def downgrade():
    op.drop_constraint('post_users_fk' , table_name='posts')
    op.drop_column('posts' , 'owner_id')
    pass
