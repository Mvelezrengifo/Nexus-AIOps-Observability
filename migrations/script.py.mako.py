"""create_insights_table

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2026-05-25 10:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ai_insights',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('anomaly_type', sa.String(50), nullable=True),
        sa.Column('source_service', sa.String(100), nullable=False),
        sa.Column('recommendation_level', sa.String(20), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ai_insights_timestamp', 'ai_insights', ['timestamp'])


def downgrade() -> None:
    op.drop_index('ix_ai_insights_timestamp', table_name='ai_insights')
    op.drop_table('ai_insights')