"""add foreign key to post table

Revision ID: 94a2f7b78d90
Revises: 84f29b7fd2b3
Create Date: 2021-11-23 00:55:04.055306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94a2f7b78d90'
down_revision = '84f29b7fd2b3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fkey', 
                            source_table="posts", 
                            referent_table="users",
                            local_cols=["owner_id"],
                            remote_cols=["id"],
                            ondelete="CASECADE"
                            )
    pass


def downgrade():
    op.drop_constraint('post_users_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
