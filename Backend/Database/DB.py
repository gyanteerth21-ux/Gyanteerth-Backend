from sqlalchemy import create_engine, Column, Integer, String, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.pool import QueuePool
import os

# Automatically find the .env file in parent directories
load_dotenv(find_dotenv())

db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set. "
        "Please add it in Vercel Project Settings → Environment Variables."
    )

DB_URL = db_url
engine = create_engine(
    DB_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
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
