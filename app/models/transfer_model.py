from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from uuid_extensions import uuid7
from datetime import datetime
from typing import Optional
from .transferType_model import TransferType
if TYPE_CHECKING:
    from .wallet_model import Wallet

class Transfer(SQLModel, table=True):
    transfer_id: UUID = Field(primary_key=True, default_factory=uuid7)
    friendly_code: str = Field(nullable=False)
    amount: float = Field(nullable=False)
    paid_at: datetime = Field(nullable=False)
    is_scheduled: bool = Field(default=False)
    scheduled_date: datetime | None = Field(default=None)

    origin_wallet_id: UUID = Field(foreign_key="wallet.wallet_id", nullable=False)
    target_wallet_id: UUID | None = Field(foreign_key="wallet.wallet_id")
    transfer_type_id: UUID = Field(foreign_key="transfertype.transfer_type_id", nullable=False)

    origin_wallet: "Wallet" = Relationship(
        back_populates="sent_transfers",
        sa_relationship_kwargs={"foreign_keys": "[Transfer.origin_wallet_id]"},
    )
    target_wallet: Optional["Wallet"] = Relationship(
        back_populates="received_transfers",
        sa_relationship_kwargs={"foreign_keys": "[Transfer.target_wallet_id]"},
    )
