"""change idel

Revision ID: 7dd8fdc1634f
Revises: 14a72d2c55be
Create Date: 2020-10-31 11:28:33.467963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dd8fdc1634f'
down_revision = '14a72d2c55be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'user_id')
    # ### end Alembic commands ###
