from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

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