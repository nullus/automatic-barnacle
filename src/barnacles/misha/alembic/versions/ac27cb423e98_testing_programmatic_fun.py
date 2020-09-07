"""Testing programmatic fun

Revision ID: ac27cb423e98
Revises: 
Create Date: 2020-07-30 11:35:11.505519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac27cb423e98'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('misha_mediaitem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hash', sa.Binary(), nullable=False),
    sa.Column('path', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sqlite_autoincrement=True
    )
    op.create_index(op.f('ix_misha_mediaitem_hash'), 'misha_mediaitem', ['hash'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_misha_mediaitem_hash'), table_name='misha_mediaitem')
    op.drop_table('misha_mediaitem')
    # ### end Alembic commands ###