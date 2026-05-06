from sqlalchemy import create_engine, Column, Integer, String, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy.engine import Engine
from sqlalchemy.pool import NullPool
import time
import os

from pathlib import Path
# Look for .env in the Backend directory (one level up from Database/)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set. "
        "Please add it in Vercel Project Settings → Environment Variables."
    )

DB_URL = db_url
engine = create_engine(
    DB_URL,
    poolclass=NullPool,           # REQUIRED for Vercel serverless — no persistent connections
    connect_args={
        "connect_timeout": 10,    # fail fast instead of hanging
        "gssencmode": "disable",  # prevents IPv6/GSSAPI negotiation that fails on Vercel
        "sslmode": "prefer",     # 'prefer' works for both Supabase (SSL) and local DB (none)
    },
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

query_times = []

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    query_times.append(total)
