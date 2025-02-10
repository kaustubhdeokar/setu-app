from app.auth.db_config import DATABASE_URL
from app.models import Base, User, Analytics
from app.schemas import AnalyticsResponse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import time

engine = None
SessionLocal = None

def init_db():
    global engine, SessionLocal
    for _ in range(5): # retrying for 5 times.
        try:
            engine = create_engine(DATABASE_URL)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            print("Connected to the database successfully!")
            Base.metadata.create_all(bind=engine, checkfirst=True)
            break
        except Exception as e:
            print("Database connection failed, retrying in 5 seconds...")
            print(f"Error: {e}")
            time.sleep(5)

def get_db():
    if SessionLocal is None:
        raise Exception("Database not initialized. Call init_db() first.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_analytics_data(db):
    analytics_entries = db.query(Analytics).all()
    return [AnalyticsResponse(
        id=entry.id,
        username=entry.username,
        pass_kyc=entry.pass_kyc,
        fail_kyc=entry.fail_kyc,
        pass_bank=entry.pass_bank,
        fail_bank=entry.fail_bank,
        total_pass=entry.total_fail,
        total_fail=entry.total_fail)
        for entry in analytics_entries]