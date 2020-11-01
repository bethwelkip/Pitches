"""change id

Revision ID: c8927413006e
Revises: 4acbfded49f9
Create Date: 2020-10-30 06:47:03.084939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8927413006e'
down_revision = '4acbfded49f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_column('users', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('users', 'id')
    # ### end Alembic commands ###
