"""drop items table

Revision ID: d994f4a42776
Revises: e3b9160c9f83
Create Date: 2021-07-07 04:48:44.875022

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "d994f4a42776"
down_revision = "e3b9160c9f83"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("item")


def downgrade():
    pass
