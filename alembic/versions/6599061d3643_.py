"""empty message

Revision ID: 6599061d3643
Revises: b8754f0e7863
Create Date: 2020-07-21 16:01:59.680207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6599061d3643'
down_revision = 'b8754f0e7863'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('barnacles_mediaitem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hash', sa.Binary(), nullable=False),
    sa.Column('path', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hash'),
    sqlite_autoincrement=True
    )
    op.create_index(op.f('ix_barnacles_mediaitem_hash'), 'barnacles_mediaitem', ['hash'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_barnacles_mediaitem_hash'), table_name='barnacles_mediaitem')
    op.drop_table('barnacles_mediaitem')
    # ### end Alembic commands ###
