from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from app.auth.db_config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT
import time
from pydantic import BaseModel, ValidationError

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
    analytics = relationship("Analytics", back_populates="user")
    

class Analytics(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), ForeignKey('users.username'), nullable=False)
    pass_kyc = Column(Integer, default=0)
    fail_kyc = Column(Integer, default=0)
    pass_bank = Column(Integer, default=0)
    fail_bank = Column(Integer, default=0)
    total_pass = Column(Integer, default=0)
    total_fail = Column(Integer, default=0)
    user = relationship("User", back_populates="analytics")

def get_db():
    if SessionLocal is None:
        raise Exception("Database not initialized. Call init_db() first.")    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AnalyticsResponse(BaseModel):
    id: int
    username: str
    pass_kyc: int
    fail_kyc: int
    pass_bank: int
    fail_bank: int
    total_pass: int
    total_fail: int
    
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