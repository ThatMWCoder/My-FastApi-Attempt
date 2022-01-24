"""create posts table

Revision ID: 05f8e4638795
Revises: 
Create Date: 2022-01-04 11:33:28.318267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05f8e4638795'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id",sa.Integer(), nullable=False, primary_key=True),
    sa.Column("title", sa.String(), nullable=False)
    )

def downgrade():
    op.drop_table("posts")
