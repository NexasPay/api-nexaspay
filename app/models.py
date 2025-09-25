from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .db import Base
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    sub = Column(String, unique=True, index=True)  
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    wallets = relationship("Wallet", back_populates="owner")


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="wallets")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    from_wallet = Column(String, index=True)
    to_wallet = Column(String, index=True)
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="pending")
    meta = Column(JSON, default={})
    hash = Column(String, nullable=True)
    fraud_score = Column(Float, default=0.0)
