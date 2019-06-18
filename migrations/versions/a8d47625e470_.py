"""empty message

Revision ID: a8d47625e470
Revises: f8cd4e260151
Create Date: 2019-06-18 13:50:20.407763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8d47625e470'
down_revision = 'f8cd4e260151'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_username'), 'admin', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_admin_username'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###
