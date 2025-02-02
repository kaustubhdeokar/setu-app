from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.auth.db_config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT
import time

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = None
SessionLocal = None
Base = declarative_base()

def init_db():
    for _ in range(10):  # Retry up to 10 times
        try:
            global engine, SessionLocal
            engine = create_engine(DATABASE_URL)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            print("Connected to the database successfully!")
            Base.metadata.create_all(bind=engine, checkfirst=True)
            break
        except Exception as e:
            print("Database connection failed, retrying in 5 seconds...")
            print(f"Error: {e}")
            time.sleep(5)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))
    pan_number = Column(String(10), unique=True)

class Analytics(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True, index=True)
    

def get_db():
    if SessionLocal is None:
        raise Exception("Database not initialized. Call init_db() first.")    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()