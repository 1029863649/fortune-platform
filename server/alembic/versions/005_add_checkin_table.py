"""add checkin table

Revision ID: 005
Revises: 004
Create Date: 2024-03-21 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 创建签到表
    op.create_table(
        'checkins',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('check_date', sa.Date(), nullable=False),
        sa.Column('reward', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'check_date', name='uq_user_check_date')
    )
    
    # 创建索引
    op.create_index('ix_checkins_user_date', 'checkins', ['user_id', 'check_date'])
    op.create_index('ix_checkins_date', 'checkins', ['check_date'])

def downgrade() -> None:
    op.drop_index('ix_checkins_date')
    op.drop_index('ix_checkins_user_date')
    op.drop_table('checkins') 