#This is the Database connection setup
#This is like a bridge It will connect both endss
#Connects to the actual database (SQLite) so data can be saved or retrieved

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./health.db"  # SQLite file-based DB

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

