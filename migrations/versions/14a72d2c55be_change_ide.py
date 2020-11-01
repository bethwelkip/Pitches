"""change ide

Revision ID: 14a72d2c55be
Revises: df180ccf96d1
Create Date: 2020-10-31 11:04:56.563883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14a72d2c55be'
down_revision = 'df180ccf96d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('userid', sa.Integer(), nullable=False))
    op.drop_column('users', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('users', 'userid')
    # ### end Alembic commands ###
