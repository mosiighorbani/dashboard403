"""empty message

Revision ID: 2a79877356b0
Revises: 29ccab88aef7
Create Date: 2024-06-17 11:06:03.833489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a79877356b0'
down_revision = '29ccab88aef7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('phone', sa.String(length=11), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=500), nullable=True),
    sa.Column('role', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=150), nullable=True),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###