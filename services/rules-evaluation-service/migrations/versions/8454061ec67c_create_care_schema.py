"""create_care_schema

Revision ID: 8454061ec67c
Revises: 
Create Date: 2026-04-19 13:36:57.053264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8454061ec67c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SCHEMA IF NOT EXISTS care")


def downgrade() -> None:
    """Downgrade schema."""
    # CASCADE ensures that if any tables were added later, they are removed too
    op.execute("DROP SCHEMA IF EXISTS care CASCADE")
