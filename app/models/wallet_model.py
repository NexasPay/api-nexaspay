from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from uuid_extensions import uuid7
from .user_model import User
from .walletType_model import Wallet_Type
if TYPE_CHECKING:
    from .transfer_model import Transfer

class Wallet(SQLModel, table=True):
    wallet_id: UUID = Field(primary_key=True, default_factory=uuid7)
    friendly_code: str = Field(nullable=False)
    money: float = Field(default=0.0)
    is_deleted: bool = Field(default=False)

    user_id: UUID = Field(foreign_key="User.user_id", nullable=False)
    wallet_type_id: UUID = Field(foreign_key="Wallet_Type.wallet_type_id", nullable=False)

    user: "User" = Relationship()
    wallet_type: "Wallet_Type" = Relationship()
    transactions: list["Transfer"] = Relationship(back_populates="origin_wallet")