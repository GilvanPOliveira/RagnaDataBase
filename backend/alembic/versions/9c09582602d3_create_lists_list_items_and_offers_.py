"""create lists, list_items and offers tables

Revision ID: 9c09582602d3
Revises: None
Create Date: 2025-07-14 19:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9c09582602d3'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'lists',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('now()'), nullable=False),
    )
    op.create_table(
        'list_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('list_id', sa.Integer, sa.ForeignKey('lists.id', ondelete='CASCADE'), nullable=False),
        sa.Column('item_id', sa.Integer, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False, server_default="1"),
        sa.Column('added_at', sa.DateTime, server_default=sa.text('now()'), nullable=False),
    )
    op.create_table(
        'offers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('item_id', sa.Integer, nullable=False, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('price', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('now()'), nullable=False),
    )

def downgrade():
    op.drop_table('offers')
    op.drop_table('list_items')
    op.drop_table('lists')
