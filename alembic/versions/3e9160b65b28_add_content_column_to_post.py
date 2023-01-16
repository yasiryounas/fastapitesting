"""add content column to post

Revision ID: 3e9160b65b28
Revises: 218590f44fd5
Create Date: 2023-01-16 22:42:25.308215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e9160b65b28'
down_revision = '218590f44fd5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
