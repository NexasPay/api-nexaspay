from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from uuid_extensions import uuid7
from datetime import datetime
from .transferType_model import TransactionType
if TYPE_CHECKING:
    from .wallet_model import Wallet

class Transfer(SQLModel, table=True):
    transaction_id: UUID = Field(primary_key=True, default_factory=uuid7)
    friendly_code: str = Field(nullable=False)
    amount: float = Field(nullable=False)
    paid_at: datetime = Field(nullable=False)
    is_scheduled: bool = Field(default=False)
    scheduled_date: datetime | None = Field(default=None)

    origin_wallet_id: UUID = Field(foreign_key="Wallet.wallet_id", nullable=False)
    target_wallet_id: UUID | None = Field(foreign_key="Wallet.wallet_id")
    transaction_type_id: UUID = Field(foreign_key="TransactionType.transaction_type_id", nullable=False)

    origin_wallet: "Wallet" = Relationship(back_populates="transactions")
    target_wallet: "Wallet" = Relationship()
