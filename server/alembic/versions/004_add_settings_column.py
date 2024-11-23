"""add settings column to user table

Revision ID: 004
Revises: 003
Create Date: 2024-03-21 17:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 添加settings列
    op.add_column('users', sa.Column('settings', postgresql.JSON, nullable=True))
    
    # 设置默认值
    op.execute("""
        UPDATE users 
        SET settings = '{
            "email_notification": true,
            "browser_notification": false,
            "public_history": false,
            "public_favorites": false,
            "theme": "light"
        }'::jsonb
        WHERE settings IS NULL
    """)
    
    # 设置非空约束
    op.alter_column('users', 'settings',
               existing_type=postgresql.JSON,
               nullable=False)

def downgrade() -> None:
    # 删除settings列
    op.drop_column('users', 'settings') 