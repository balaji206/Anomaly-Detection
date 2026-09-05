import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Defaults to a local SQLite file — zero setup, no cloud/Postgres needed for the demo.
# To match your tech-stack slide later, just point this at a Postgres URL instead,
# e.g. postgresql://user:pass@localhost:5432/aws_anomaly — nothing else in the app changes.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aws_anomaly.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
