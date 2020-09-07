"""Rename table

Revision ID: a369f7557e85
Revises: ac27cb423e98
Create Date: 2020-07-30 12:23:22.086829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a369f7557e85'
down_revision = 'ac27cb423e98'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('misha_mediaitem', 'misha_addresspath')


def downgrade():
    op.rename_table('misha_addresspath', 'misha_mediaitem')
