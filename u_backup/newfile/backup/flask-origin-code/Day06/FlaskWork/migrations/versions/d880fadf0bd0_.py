"""empty message

Revision ID: d880fadf0bd0
Revises: 37361e74bd6a
Create Date: 2019-05-21 15:24:57.418940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd880fadf0bd0'
down_revision = '37361e74bd6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movie',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('postid', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('image', sa.String(length=256), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movie')
    # ### end Alembic commands ###