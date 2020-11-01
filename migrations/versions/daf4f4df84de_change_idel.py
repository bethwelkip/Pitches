"""change idel

Revision ID: daf4f4df84de
Revises: 4adcf04c0f03
Create Date: 2020-10-31 14:06:49.304771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daf4f4df84de'
down_revision = '4adcf04c0f03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('pitch_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'pitches', ['pitch_id'], ['pitch_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'pitch_id')
    # ### end Alembic commands ###