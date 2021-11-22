"""add user table

Revision ID: 84f29b7fd2b3
Revises: 6033ce3a0e5f
Create Date: 2021-11-23 00:46:15.422598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84f29b7fd2b3'
down_revision = '6033ce3a0e5f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('email', sa.String(), nullable=False),
                            sa.Column('password', sa.String(), nullable=False),
                            sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                        server_default=sa.text('now()'),
                                        nullable=True),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')
                            )
    pass


def downgrade():
    op.drop_table('users')
    pass
