from sqlmodel import Field, SQLModel
from uuid import UUID
from uuid_extensions import uuid7
from .enums_model import WalletTypeEnum

class Wallet_Type(SQLModel, table=True):
    wallet_type_id: UUID = Field(primary_key=True, default_factory=uuid7)
    name: WalletTypeEnum = Field(default=WalletTypeEnum.DEFAULT)