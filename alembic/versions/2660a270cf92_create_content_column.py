"""create content column

Revision ID: 2660a270cf92
Revises: 05f8e4638795
Create Date: 2022-01-04 11:46:28.019118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2660a270cf92'
down_revision = '05f8e4638795'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", 'content')
