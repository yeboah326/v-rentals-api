"""empty message

Revision ID: 9c34a7e531cd
Revises: 54f00ea17d53
Create Date: 2022-05-03 16:39:54.968670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c34a7e531cd'
down_revision = '54f00ea17d53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vr_vehicle', sa.Column('registration_number', sa.String(length=30), nullable=True))
    op.execute("UPDATE vr_vehicle SET registration_number = 'XX-XXXX-XX'")
    op.alter_column('vr_vehicle', 'registration_number', nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vr_vehicle', 'registration_number')
    # ### end Alembic commands ###