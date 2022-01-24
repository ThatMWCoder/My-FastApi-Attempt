"""Add foreign key to posts table

Revision ID: 46667b194058
Revises: b23707c31cc1
Create Date: 2022-01-05 15:15:50.900516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46667b194058'
down_revision = 'b23707c31cc1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users",
                          local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
