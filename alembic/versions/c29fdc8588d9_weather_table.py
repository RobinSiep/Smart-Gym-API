"""weather table

Revision ID: c29fdc8588d9
Revises: 9076b07a023c
Create Date: 2016-05-24 15:22:34.928780

"""

# revision identifiers, used by Alembic.
revision = 'c29fdc8588d9'
down_revision = '9076b07a023c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weather',
                    sa.Column(
                        'id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
                    sa.Column(
                        'date', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('raining_outside', sa.Boolean(), nullable=True),
                    sa.Column(
                        'temperature', sa.Float(precision=1), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('sport_schedule',
                    sa.Column(
                        'id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
                    sa.Column(
                        'user_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
                    sa.Column('name', sa.String(length=100), nullable=True),
                    sa.Column('reminder_minutes', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint(
                        'user_id', 'name', name='sport_schedule_name_uc')
                    )
    op.add_column('user_activity', sa.Column(
        'weather_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True))
    op.create_foreign_key(
        None, 'user_activity', 'weather', ['weather_id'], ['id'])
    op.drop_column('user_activity', 'temperature')
    op.drop_column('user_activity', 'raining_outside')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_activity', sa.Column(
        'raining_outside', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('user_activity', sa.Column(
        'temperature', sa.REAL(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user_activity', type_='foreignkey')
    op.drop_column('user_activity', 'weather_id')
    op.drop_table('sport_schedule')
    op.drop_table('weather')
    ### end Alembic commands ###
