"""empty message

Revision ID: 8bc157914a89
Revises: 9eb3f302a690
Create Date: 2021-03-31 16:57:36.117487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bc157914a89'
down_revision = '9eb3f302a690'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    Print('nicht noetig')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('looking_for_venue', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('Artist', 'seeking_talent')
    # ### end Alembic commands ###
