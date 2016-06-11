"""create sport schedule table

Revision ID: c524415f25c1
Revises: 100383d009f0
Create Date: 2016-04-24 15:26:15.971964

"""

# revision identifiers, used by Alembic.
revision = 'c524415f25c1'
down_revision = '100383d009f0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sport_schedule',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('reminder_minutes', sa.Integer(), nullable=True),
    sa.Column('datetime', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sport_schedule')
    ### end Alembic commands ###
