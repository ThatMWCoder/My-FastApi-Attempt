"""Create fully fledged post table

Revision ID: 799bd818df84
Revises: 46667b194058
Create Date: 2022-01-05 15:36:15.933909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '799bd818df84'
down_revision = '46667b194058'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text("NOW()"))) 


def downgrade():
    op.drop_column("posts", "created_at")
