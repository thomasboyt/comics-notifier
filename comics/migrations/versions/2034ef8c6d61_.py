"""Add key field

Revision ID: 2034ef8c6d61
Revises: 2ca217f747be
Create Date: 2013-05-25 18:06:06.947249

"""

# revision identifiers, used by Alembic.
revision = '2034ef8c6d61'
down_revision = '2ca217f747be'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'user',
        sa.Column('key', sa.String(24))
    )
    pass


def downgrade():
    pass
