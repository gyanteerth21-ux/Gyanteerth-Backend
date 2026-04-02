from sqlalchemy import create_engine, Column, Integer, String, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy.engine import Engine
import time
import os

load_dotenv()
db_url = os.environ["DATABASE_URL"]

DB_URL= db_url
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
session=SessionLocal(bind=engine)

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
