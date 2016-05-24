"""device revisions

Revision ID: 9076b07a023c
Revises: 2cb0992ff4ab
Create Date: 2016-05-20 17:03:39.588260

"""

# revision identifiers, used by Alembic.
revision = '9076b07a023c'
down_revision = '2cb0992ff4ab'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('device_address', sa.String(length=17), nullable=True),
    sa.Column('device_class', sa.Integer, nullable=True),
    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
    sa.Column('last_used', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('device_address')
    )
    op.add_column('gym', sa.Column('MAC_address', sa.String(length=17), nullable=True))
    op.create_unique_constraint(None, 'gym', ['MAC_address'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'gym', type_='unique')
    op.drop_column('gym', 'MAC_address')
    op.drop_table('device')
    ### end Alembic commands ###
