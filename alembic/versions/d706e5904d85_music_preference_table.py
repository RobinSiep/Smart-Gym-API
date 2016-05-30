"""music preference table

Revision ID: d706e5904d85
Revises: c29fdc8588d9
Create Date: 2016-05-30 15:24:47.082457

"""

# revision identifiers, used by Alembic.
revision = 'd706e5904d85'
down_revision = 'c29fdc8588d9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('music_preference',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(length=16), nullable=False),
    sa.Column('artist', sa.String(length=100), nullable=True),
    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType(length=16), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('cardio_activity')
    op.drop_column('sport_schedule', 'weekdays')
    op.drop_column('sport_schedule', 'time')
    op.drop_column('sport_schedule', 'is_active')
    op.drop_column('user_activity', 'temperature')
    op.drop_column('user_activity', 'raining_outside')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_activity', sa.Column('raining_outside', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('user_activity', sa.Column('temperature', sa.REAL(), autoincrement=False, nullable=True))
    op.add_column('sport_schedule', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('sport_schedule', sa.Column('time', postgresql.TIME(timezone=True), autoincrement=False, nullable=True))
    op.add_column('sport_schedule', sa.Column('weekdays', postgresql.ARRAY(INTEGER()), autoincrement=False, nullable=True))
    op.create_table('cardio_activity',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('activity_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('start_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('end_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('distance', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('speed', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('calories', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='cardio_activity_pkey')
    )
    op.drop_table('music_preference')
    ### end Alembic commands ###
