"""Change release_date from Date to DateTime.

Revision ID: 2ca217f747be
Revises: None
Create Date: 2013-05-22 16:17:41.891189

"""

# revision identifiers, used by Alembic.
revision = '2ca217f747be'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        table_name='issue',
        column_name='release_date',
        nullable=False,
        type_=sa.types.Date()
    )
    pass


def downgrade():
    op.alter_column(
        table_name='issue',
        column_name='release_date',
        nullable=False,
        type_=sa.types.DateTime()
    )
    pass
