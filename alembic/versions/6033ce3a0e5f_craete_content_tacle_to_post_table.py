"""craete content tacle to post table

Revision ID: 6033ce3a0e5f
Revises: 06b16e958ab6
Create Date: 2021-11-23 00:36:06.175067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6033ce3a0e5f'
down_revision = '06b16e958ab6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
