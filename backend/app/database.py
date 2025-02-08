from app.auth.db_config import DATABASE_URL
from app.models import Base, User, Analytics

from app.schemas import AnalyticsResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
        total_fail=entry.total_fail
    ) for entry in analytics_entries]


def update_analytics(case, username, db):
    analytics_entry = db.query(Analytics).filter(Analytics.username == username).first()
    
    if not analytics_entry:
        if case == "kyc_fail":
            new_analytics_entry = Analytics(
                username=username,
                fail_kyc=1,
                total_fail=1
            )
        elif case == "bank_fail":
            new_analytics_entry = Analytics(
                username=username,
                fail_bank=1,
                total_fail=1
            )
        else:
            new_analytics_entry = Analytics(
                username=username,
                pass_kyc=1,
                pass_bank=1,
                total_pass=1
            )
        db.add(new_analytics_entry)
        db.commit()
    else:
        if case == "kyc_fail":
            analytics_entry.fail_kyc += 1
            analytics_entry.total_fail += 1
        elif case == "bank_fail":
            analytics_entry.fail_bank += 1
            analytics_entry.total_fail += 1
        else:
            analytics_entry.pass_kyc+=1
            analytics_entry.pass_bank+=1
            analytics_entry.total_pass += 1
    db.commit()