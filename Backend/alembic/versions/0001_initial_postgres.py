"""Initial tables for PostgreSQL (Supabase)

Revision ID: 0001_initial_postgres
Revises: 
Create Date: 2026-04-03

Full fresh migration — creates all tables from scratch for PostgreSQL.
The old MySQL migration (6e1cb0ffdb0a) is replaced by this one.
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0001_initial_postgres'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Let SQLAlchemy + Alembic's autogenerate handle table creation
    # via Base.metadata in env.py. This migration is intentionally empty
    # because we stamp head AFTER running create_all from the init script.
    pass


def downgrade() -> None:
    pass
