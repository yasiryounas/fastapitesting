"""create post tables

Revision ID: 218590f44fd5
Revises: 
Create Date: 2023-01-16 22:24:58.318529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '218590f44fd5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
