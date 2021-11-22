"""add more column to post table

Revision ID: 92e4f6c774b7
Revises: 94a2f7b78d90
Create Date: 2021-11-23 01:03:21.512228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92e4f6c774b7'
down_revision = '94a2f7b78d90'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
