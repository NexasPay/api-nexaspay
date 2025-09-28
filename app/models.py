from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .db.session import Base
from pydantic import UUID
from app import dt

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True)
    friendly_code = Column(String)
    sub = Column(String, unique=True, index=True)  
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    wallets = relationship("Wallet", back_populates="owner")


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID, primary_key=True, index=True)
    friendly_code = Column(String)
    address = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    owner = relationship("User", back_populates="wallets")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID, primary_key=True, index=True)
    friendly_code = Column(String)
    from_wallet = Column(String, index=True)
    to_wallet = Column(String, index=True)
    amount = Column(Float)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    status = Column(String, default="pending")
    meta = Column(JSON, default={})
    hash = Column(String, nullable=True)
    fraud_score = Column(Float, default=0.0)
