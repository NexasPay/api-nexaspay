from uuid_extensions import uuid7
from enum import Enum
from collections import defaultdict
from sqlalchemy import Integer, String, TIMESTAMP, DATETIME, ForeignKey, UUID, DECIMAL
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "User"
    
    user_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    friendly_code: Mapped[str] = mapped_column(String(8), nullable=False) # XX123456
    full_name: Mapped[str] = mapped_column(String(30), nullable=False)
    birthdate: Mapped[DATETIME] = mapped_column(DATETIME(), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), default=TIMESTAMP(True))
    profile_photo: Mapped[str | None] = mapped_column(String(20), default=None) # store the photo path from the AWS app server 
    is_deleted: Mapped[int] = mapped_column(Integer(1), default=0)

    phone_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), ForeignKey("Phone.phone_id"), nullable=False)
    
    wallets: Mapped[list["Wallet"]] = relationship(back_populates="user")
    phones: Mapped[list["Phone"] | "Phone"] = relationship(back_populates="user")

class Phone(Base):
    __tablename__ = "Phone"

    phone_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), nullable=False, primary_key=True)
    user_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), ForeignKey("User.user_id"), nullable=False)
    phone_type_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), ForeignKey("Phone_Type.phone_type_id"), nullable=False)
    number: Mapped[str] = mapped_column(String(10), nullable=False)
    is_primary: Mapped[int] = mapped_column(Integer(1), default=0, nullable=False)

    user: Mapped["User"] = relationship(back_populates="phones")
    phone_type: Mapped["Phone_Type"] = relationship(back_populates="phones")

class Phone_Type(Base):
    __tablename__ = "PhoneType"

    phone_type_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), nullable=False, primary_key=True)
    name: Mapped["PhoneTypeEnum"] = mapped_column(String(20), nullable=False)
    is_whatsapp: Mapped[int] = mapped_column(Integer(1), nullable=False, default=0)

class Wallet(Base):
    __tablename__ = "Wallet"

    wallet_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    friendly_code: Mapped[str] = mapped_column(String(8), nullable=False) # XX123456
    cash: Mapped[float] = mapped_column(DECIMAL(), default=0, nullable=False)
    is_deleted: Mapped[int] = mapped_column(Integer(1), default=0)

    user_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), ForeignKey("User.user_id"), nullable=False)
    wallet_type_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), ForeignKey("Wallet_Type.wallet_type_id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="wallets")
    wallet_type: Mapped["Wallet_Type"] = relationship(back_populates="wallet_type")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="origin_wallet", foreign_keys=["Transaction.origin_wallet_id"])

    @property
    def transactions_by_target(self) -> dict["Wallet", list["Transaction"]]:
        target = defaultdict(list)
        
        for transaction in self.transactions:
            if transaction.target_wallet:
                target[transaction.target_wallet].append(transaction)
        
        return target

class Wallet_Type(Base):
    __tablename__ = "WalletType"

    wallet_type_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    name: Mapped["WalletTypeEnum"] = mapped_column(String(10))

    wallets: Mapped[list["Wallet"]] = relationship()

class Transaction(Base):
    __tablename__ = "Transaction"

    transaction_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    friendly_code: Mapped[str] = mapped_column(String(8), nullable=False) # XX123456
    amount: Mapped[DECIMAL] = mapped_column(DECIMAL(), nullable=False)
    paid_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(), nullable=False)
    is_scheduled: Mapped[int] = mapped_column(Integer(), default=0, nullable=False)
    scheduled_date: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP())
    
    origin_wallet_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), ForeignKey("Wallet.wallet_id"), nullable=False)
    target_wallet_id: Mapped[uuid7 | None] = mapped_column(UUID(), ForeignKey("Wallet.wallet_id"), default=None)
    transaction_type_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), ForeignKey("Transaction_Type.transaction_type_id"), nullable=False)

    origin_wallet: Mapped["Wallet"] = relationship(back_populates="transactions", foreign_keys=[origin_wallet_id])

    target_wallet: Mapped["Wallet" | None] = relationship(foreign_keys=[target_wallet_id])

class Transaction_Type(Base):
    __tablename__ = "TransactionType"

    transaction_type_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    name: Mapped["TransactionTypeEnum"] = mapped_column(String(10))

    transactions: Mapped[list["Transaction"]] = relationship()

class Address(Base):
    __tablename__ = "Address"
    
    address_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    street: Mapped[str] = mapped_column(String(30), nullable=False)
    number: Mapped[int] = mapped_column(Integer(5), nullable=False)
    complement: Mapped[str | None] = mapped_column(String(30), default=None)
    cep = Mapped[str] = mapped_column(String(8), nullable=False)
    
    city_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), ForeignKey("City.city_id"))

    city: Mapped["City"] = relationship(foreign_keys=city_id)

class City(Base):
    __tablename__ = "City"
    city_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    state_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), ForeignKey("State.state_id"))

    state: Mapped["State"] = relationship(foreign_keys=state_id)


class State(Base):
    __tablename__ = "State"
    state_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    uf: Mapped[str] = mapped_column(String(2), nullable=False)

    country_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), ForeignKey("Country.country_id"))

    country: Mapped["Country"] = relationship(foreign_keys=country_id)

class Country(Base):
    __tablename__ = "Country"
    country_id: Mapped[uuid7] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    name: Mapped[str] = mapped_column(String(30), nullable=False)


class WalletTypeEnum(Enum):
    DEFAULT = "DEFAULT"
    ENTERPRISE = "ENTERPRISE"
    CRYPTO = "CRYPTO"
    POINTS = "POINTS"
    INVESTMENT = "INVESTMENT"

class TransactionTypeEnum(Enum):
    DEPOSIT = "DEPOSIT"
    PICKUP = "PICKUP" # Saque
    PAYMENT = "PAYMENT"
    TRANSFER = "TRANSFER"

class PhoneTypeEnum(Enum):
    MOBILE = "MOBILE"
    BUSINESS = "BUSINESS"
    HOME = "HOME"


