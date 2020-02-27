"""empty message

Revision ID: 37361e74bd6a
Revises: aa348986c020
Create Date: 2019-05-21 14:37:45.844017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37361e74bd6a'
down_revision = 'aa348986c020'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banner',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('image', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('banner')
    # ### end Alembic commands ###