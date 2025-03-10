"""Описание изменений

Revision ID: e04039fa74f4
Revises: 
Create Date: 2025-01-25 15:02:48.253685

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e04039fa74f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requestlog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wallet_address', sa.String(), nullable=True),
    sa.Column('bandwidth', sa.Float(), nullable=True),
    sa.Column('energy', sa.Float(), nullable=True),
    sa.Column('trx_balance', sa.Float(), nullable=True),
    sa.Column('request_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_requestlog_id'), 'requestlog', ['id'], unique=False)
    op.create_index(op.f('ix_requestlog_wallet_address'), 'requestlog', ['wallet_address'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_requestlog_wallet_address'), table_name='requestlog')
    op.drop_index(op.f('ix_requestlog_id'), table_name='requestlog')
    op.drop_table('requestlog')
    # ### end Alembic commands ###
